# ai_tools/drawing.py

import os
from PIL import Image
import requests
import base64
import io

# --- 설정 (환경 변수 또는 설정 파일로 관리 권장) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

# 사용할 기본 AI 모델 및 API 엔드포인트
DEFAULT_API_ENDPOINT = "https://api.openai.com/v1/images/generations" # DALL-E 3 엔드포인트
DEFAULT_MODEL = "dall-e-3" # DALL-E 3 모델

# --- 핵심 함수: draw ---
def draw(
    image_path: str,
    style_prompt: str,
    output_path: str = "transformed_image.png",
    api_key: str = None,
    api_endpoint: str = DEFAULT_API_ENDPOINT,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    주어진 이미지를 AI를 사용하여 특정 스타일로 변환합니다.

    Args:
        image_path (str): 변환할 원본 이미지 파일의 경로.
        style_prompt (str): 적용할 그림 스타일을 설명하는 텍스트 프롬프트 (예: "수채화 스타일", "픽셀 아트 스타일").
        output_path (str): 변환된 이미지를 저장할 경로. 기본값은 "transformed_image.png".
        api_key (str, optional): 사용할 AI API 키. None인 경우 환경 변수 'OPENAI_API_KEY'를 사용.
        api_endpoint (str): 이미지를 생성할 AI API의 엔드포인트 URL.
        model (str): 사용할 AI 모델의 이름.

    Returns:
        str: 변환된 이미지 파일이 저장된 경로. 변환 실패 시 None.
    """
    if not os.path.exists(image_path):
        print(f"오류: 원본 이미지 파일 '{image_path}'를 찾을 수 없습니다. 경로를 확인해주세요.")
        return None

    key_to_use = api_key if api_key else OPENAI_API_KEY
    if not key_to_use:
        print("경고: API 키가 설정되지 않았습니다. 'api_key' 매개변수를 전달하거나 환경 변수 'OPENAI_API_KEY'를 설정하세요.")
        return None

    headers = {
        "Authorization": f"Bearer {key_to_use}",
        "Content-Type": "application/json",
    }

    combined_prompt = f"Imagine an image with the content of '{image_path}' and render it in a {style_prompt}. Focus purely on the artistic style change while preserving the original subject matter."

    payload = {
        "model": model,
        "prompt": combined_prompt,
        "n": 1,
        "size": "1024x1024",
    }

    try:
        print(f"DEBUG: AI API (Image) 호출 시도 - 모델: '{model}', 프롬프트: '{combined_prompt}'")

        # --- 임시 더미 응답 ---
        generated_image_url = "https://via.placeholder.com/1024x1024.png?text=AI+Styled+Image"
        print(f"DEBUG: API 호출 시뮬레이션 - 가상 이미지 URL: {generated_image_url}")

        # --- 임시 더미 이미지 파일 생성 및 저장 ---
        dummy_img = Image.new('RGB', (512, 512), color='blue')
        dummy_img.save(output_path)
        print(f"DEBUG: 변환된 이미지를 '{output_path}'에 더미로 저장했습니다.")

        return output_path

    except requests.exceptions.RequestException as e:
        print(f"오류: API 호출 중 네트워크 또는 HTTP 오류 발생: {e}")
        if e.response:
            print(f"응답 본문: {e.response.text}")
        return None
    except Exception as e:
        print(f"오류: 이미지 변환 중 예기치 않은 오류 발생: {e}")
        return None