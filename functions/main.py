# functions/main.py

# functions/main.py

# 표준 라이브러리
import os
import json # JSON 데이터 처리를 위해 필요
import io
import base64
from io import BytesIO # 이미지 처리 시 바이트 스트림을 위해 필요

# 서드파티 라이브러리
import openai # OpenAI API (DALL-E 3) 사용을 위해 필요
import google.generativeai as genai # Google Gemini API 사용을 위해 필요
from dotenv import load_dotenv # 로컬 개발 환경에서 .env 파일 로드를 위해 필요
from PIL import Image # 이미지 처리를 위해 필요

# Firebase Functions 관련 모듈
from firebase_functions import https_fn
from firebase_admin import initialize_app # Firebase Admin SDK 초기화를 위해 필요

# Firebase Admin SDK 초기화 (함수 실행 시 한 번만 초기화되도록)
# 주의: 이 코드는 main.py 파일 내에서 @https_fn.on_request() 바깥에 위치해야 합니다.
try:
    initialize_app()
except ValueError:
    # 이미 초기화된 경우 (예: 에뮬레이터에서 여러 함수를 로드할 때) 오류를 무시합니다.
    pass

# AI 관련 모듈
import google.generativeai as genai
import openai
from dotenv import load_dotenv # 로컬 개발 환경에서만 사용

# Firebase Admin SDK 초기화 (대부분의 경우 자동으로 초기화되므로 필요 없음)
# initialize_app()

# --- API 키 설정 ---
# 1. 로컬 환경 (.env 파일) 또는 Firebase 에뮬레이터에서 실행 중일 때:
#    .env 파일에서 OPENAI_API_KEY와 GEMINI_API_KEY를 로드합니다.
# 2. 실제 Firebase Cloud Functions에 배포되었을 때:
#    firebase functions:config:set 이나 firebase functions:secrets:set 명령어로 설정된
#    환경 변수를 os.getenv()를 통해 직접 로드합니다.
#    (예: `firebase functions:config:set openai.key="YOUR_OPENAI_KEY" gemini.key="YOUR_GEMINI_KEY"`로 설정했다면
#     `OPEN_AI_KEY`와 `GEMINI_KEY` 변수로 노출될 가능성이 높습니다.
#     실제 사용하는 환경 변수 이름은 당신이 Firebase에 설정한 이름에 따라 달라집니다.)

if os.getenv("FUNCTIONS_EMULATOR") == "true":
    load_dotenv() # .env 파일에서 환경 변수 로드
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
else:
    # 실제 Firebase Functions 환경에서는 os.getenv()로 직접 API 키를 가져옵니다.
    # 여기서는 firebase functions:config:set 명령어로 설정했을 때의 일반적인 변수명 패턴을 따릅니다.
    OPENAI_API_KEY = os.getenv("OPEN_AI_KEY") # 실제 설정한 변수명과 일치해야 합니다.
    GEMINI_API_KEY = os.getenv("GEMINI_KEY") # 실제 설정한 변수명과 일치해야 합니다.

# API 클라이언트 초기화
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_VISION_MODEL = 'gemini-1.5-flash'
GEMINI_PRO_MODEL = 'gemini-1.5-flash'


# --- 이미지 변환 로직 (drawing.py에서 가져옴) ---
def get_image_description(image_data: bytes, user_prompt: str = "") -> str | None:
    """
    Gemini Vision API를 사용하여 이미지 내용을 설명합니다.
    """
    try:
        model = genai.GenerativeModel(GEMINI_VISION_MODEL)
        img = Image.open(BytesIO(image_data))

        prompt_parts = [
            "이 이미지를 상세히 설명해 주세요. 어떤 스타일, 색상, 객체, 분위기 등이 있는지 포함하여 DALL-E 3가 새로운 이미지를 생성할 수 있도록 자세하고 구체적으로 묘사해주세요. 불필요한 서두나 결론 문구 없이 이미지 묘사만 해주세요. 설명의 길이는 500자를 넘지 않도록 해주세요."
        ]
        if user_prompt:
            prompt_parts.insert(0, user_prompt) # 사용자 프롬프트를 맨 앞에 추가

        response = model.generate_content(prompt_parts + [img]) # 리스트 병합

        description = response.text.strip()
        return description

    except Exception as e:
        print(f"Error getting image description from Gemini: {e}")
        return None

def generate_dalle_image(prompt: str, size: str = "1024x1024", quality: str = "standard") -> str | None:
    """
    DALL-E 3 API를 사용하여 이미지를 생성하고 URL을 반환합니다.
    """
    try:
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1
        )
        image_url = response.data[0].url
        print(f"DEBUG: Raw DALL-E response URL: {image_url}")
        return image_url
    except openai.APIError as e:
        print(f"OpenAI API Error: {e.response.status_code} - {e.response.json()}")
        return None
    except Exception as e:
        print(f"Error generating DALL-E image: {e}")
        return None

# --- Cloud Function: 이미지 스타일 변환 ---
@https_fn.on_request()
def stylize_image(request: https_fn.Request) -> https_fn.Response:
    """
    HTTP POST 요청을 받아 이미지를 스타일 변환하고 결과를 반환하는 Cloud Function.

    요청 형식 (JSON):
    {
        "image_data": "base64로 인코딩된 이미지 데이터 (필수)",
        "style_prompt": "원하는 스타일 (예: 'oil painting', 'pixel art') (필수)",
        "user_prompt": "이미지에 대한 추가 설명 또는 질문 (선택 사항)"
    }
    """
    if request.method != 'POST':
        return https_fn.Response("Method Not Allowed. Please send a POST request.", status=405)

    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return https_fn.Response("Bad Request: JSON body is required.", status=400)

        image_data_b64 = request_json.get('image_data')
        style_prompt = request_json.get('style_prompt')
        user_prompt = request_json.get('user_prompt', '')

        if not image_data_b64 or not style_prompt:
            return https_fn.Response("Bad Request: Missing 'image_data' or 'style_prompt'.", status=400)

        image_data = base64.b64decode(image_data_b64)

        # 1. Gemini로 이미지 설명 얻기
        gemini_description = get_image_description(image_data, user_prompt)
        if not gemini_description:
            return https_fn.Response("Internal Server Error: Failed to get image description from Gemini.", status=500)

        # 2. DALL-E 프롬프트 구성
        dalle_prompt = f"{gemini_description}. 이 이미지를 {style_prompt} 스타일로 그려줘. 고품질의 예술적인 이미지를 생성해줘."

        # 3. DALL-E 3로 이미지 생성 및 URL 얻기
        image_url = generate_dalle_image(dalle_prompt)
        print(f"DEBUG: DALL-E generated URL: {image_url}")

        if image_url:
            return https_fn.Response(
                json.dumps({"message": "Image stylized successfully!", "image_url": image_url}),
                status=200,
                headers={"Content-Type": "application/json"}
            )
        else:
            return https_fn.Response("Internal Server Error: Failed to generate DALL-E 3 image.", status=500)

    except Exception as e:
        print(f"Error in stylize_image function: {e}")
        return https_fn.Response(json.dumps({"message": f"Internal Server Error: {e}"}),
            f"Internal Server Error: {e}", status=500)


# --- 챗봇 로직 (chatbot.py에서 가져옴) ---
def get_gemini_text_response(prompt: str) -> str | None:
    """
    Gemini Pro 모델을 사용하여 텍스트 응답을 생성합니다.
    """
    try:
        model = genai.GenerativeModel(GEMINI_PRO_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting text response from Gemini: {e}")
        return None

# --- Cloud Function: 챗봇 (텍스트 전용) ---
@https_fn.on_request()
def chat_with_gemini(request: https_fn.Request) -> https_fn.Response:
    """
    HTTP POST 요청을 받아 Gemini 챗봇으로 텍스트 응답을 반환하는 Cloud Function.

    요청 형식 (JSON):
    {
        "prompt": "사용자 질문"
    }
    """
    if request.method != 'POST':
        return https_fn.Response("Method Not Allowed. Please send a POST request.", status=405)

    try:
        request_json = request.get_json(silent=True)
        if not request_json or 'prompt' not in request_json:
            return https_fn.Response("Bad Request: JSON body with 'prompt' is required.", status=400)

        user_prompt = request_json.get('prompt')

        response_text = get_gemini_text_response(user_prompt)

        if response_text:
            return https_fn.Response(
                json.dumps({"message": "Chatbot response generated successfully!", "response_text": response_text}),
                status=200,
                headers={"Content-Type": "application/json"}
            )
        else:
            return https_fn.Response(json.dumps({"message": "Internal Server Error: Failed to get chatbot response."}),
                "Internal Server Error: Failed to get chatbot response.", status=500)

    except Exception as e:
        print(json.dumps({"message": f"Internal Server Error: {e}"}),
            f"Error in chat_with_gemini function: {e}")
        return https_fn.Response(f"Internal Server Error: {e}", status=500) 