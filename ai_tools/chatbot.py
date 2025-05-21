# ai_tools/chatbot.py

import os
import google.generativeai as genai
from PIL import Image

# --- 설정 (환경 변수 또는 설정 파일로 관리 권장) ---
# 실제 API 키는 절대 코드에 직접 노출하지 마세요!
# .env 파일에서 불러옵니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

# 챗봇 모델 (텍스트 전용)
DEFAULT_TEXT_MODEL = "gemini-1.5-flash"
# 멀티모달 챗봇 모델 (이미지 + 텍스트)
DEFAULT_VISION_MODEL = "gemini-1.5-flash"

# --- API 키 설정 및 Gemini 클라이언트 구성 ---
def _configure_gemini(api_key: str = None):
    """
    Gemini API 클라이언트를 설정합니다.
    API 키가 전달되면 그 키를 사용하고, 없으면 환경 변수를 사용합니다.
    """
    key_to_use = api_key if api_key else GEMINI_API_KEY 
    
    if not key_to_use:
        print("경고: Gemini API 키가 설정되지 않았습니다. API 호출이 실패할 수 있습니다.")
        print("환경 변수 'GEMINI_API_KEY'를 설정하거나 함수에 직접 API 키를 전달하세요.")
        return False
    
    try:
        genai.configure(api_key=key_to_use)
        return True
    except Exception as e:
        print(f"Gemini API 설정 중 오류 발생: {e}")
        return False

# --- 핵심 함수: 텍스트 기반 대화 ---
def ask_text(
    question: str,
    model: str = DEFAULT_TEXT_MODEL,
    api_key: str = None,
) -> str:
    """
    텍스트 기반 질문에 대해 AI 챗봇의 답변을 요청합니다.

    Args:
        question (str): 사용자 질문 (텍스트).
        model (str): 사용할 텍스트 기반 Gemini 모델의 이름.
        api_key (str, optional): 사용할 Gemini API 키. None인 경우 환경 변수를 사용.

    Returns:
        str: AI 챗봇의 답변. 실패 시 None.
    """
    if not _configure_gemini(api_key):
        return None

    try:
        gemini_model = genai.GenerativeModel(model)
        print(f"DEBUG: AI API (Chatbot Text) 호출 시도 - 모델: '{model}', 질문: '{question[:30]}...'")
        response = gemini_model.generate_content(question)
        
        # 응답 처리 (안전성 검사 등)
        if response and response.candidates:
            return response.text
        else:
            print("경고: Gemini API로부터 유효한 답변을 받지 못했습니다.")
            return None
    except Exception as e:
        print(f"오류: 챗봇 질문 처리 중 오류 발생: {e}")
        return None

# --- 핵심 함수: 멀티모달 (이미지 + 텍스트) 대화 ---
def ask_vision(
    image_path: str,
    question: str,
    model: str = DEFAULT_VISION_MODEL,
    api_key: str = None,
) -> str:
    """
    이미지와 텍스트를 함께 포함하는 질문에 대해 AI 챗봇의 답변을 요청합니다.

    Args:
        image_path (str): 질문과 함께 제공할 이미지 파일의 경로.
        question (str): 이미지에 대한 사용자 질문 (텍스트).
        model (str): 사용할 멀티모달 Gemini 모델의 이름.
        api_key (str, optional): 사용할 Gemini API 키. None인 경우 환경 변수를 사용.

    Returns:
        str: AI 챗봇의 답변. 실패 시 None.
    """
    if not os.path.exists(image_path):
        print(f"오류: 이미지 파일 '{image_path}'를 찾을 수 없습니다. 경로를 확인해주세요.")
        return None

    if not _configure_gemini(api_key):
        return None

    try:
        img = Image.open(image_path) # PIL Image 객체로 로드
        gemini_model = genai.GenerativeModel(model)
        
        print(f"DEBUG: AI API (Chatbot Vision) 호출 시도 - 모델: '{model}', 이미지: '{image_path}', 질문: '{question[:30]}...'")
        response = gemini_model.generate_content([img, question])

        if response and response.candidates:
            return response.text
        else:
            print("경고: Gemini Vision API로부터 유효한 답변을 받지 못했습니다.")
            return None
    except Exception as e:
        print(f"오류: 비전 챗봇 질문 처리 중 오류 발생: {e}")
        return None