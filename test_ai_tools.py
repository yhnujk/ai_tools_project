# test_ai_tools.py
import ai_tools.drawing
import ai_tools.chatbot
import os
from PIL import Image

# .env 파일에서 환경 변수 로드
# 이 줄이 있어야 .env 파일에 저장된 API 키를 코드에서 사용할 수 있습니다.
from dotenv import load_dotenv
load_dotenv() 

print("--- AI-Tools 라이브러리 통합 테스트 시작 ---")

# --- 1. Drawing 모듈 테스트 ---
print("\n--- Drawing 모듈 테스트 ---")
# 테스트를 위한 더미 이미지 파일 생성 (실제 이미지 경로로 변경 가능)
# 이 파일은 test_ai_tools.py가 실행되는 ai_tools_project 폴더에 생성됩니다.
dummy_input_image_path = "test_input_image_for_drawing.png"
try:
    Image.new('RGB', (200, 200), color = 'red').save(dummy_input_image_path)
    print(f"더미 입력 이미지 생성: {dummy_input_image_path}")
except Exception as e:
    print(f"오류: 더미 이미지 생성 실패: {e}")
    dummy_input_image_path = None # 이미지 생성 실패 시 None으로 설정

if dummy_input_image_path:
    user_drawing_style = input("🎨 원하는 그림체 스타일을 입력하세요 (예: 유화, 픽셀아트, 수묵화): ")

    # AI-Tools 라이브러리 drawing 모듈 호출
    # 현재 drawing.py는 실제 API 호출 대신 더미 이미지를 생성합니다.
    # API 키가 올바르게 설정되면 실제 DALL-E 호출로 대체될 수 있습니다.
    output_drawing_path = ai_tools.drawing.draw(
        image_path=dummy_input_image_path,
        style_prompt=user_drawing_style,
        output_path="my_styled_artwork.png" # 생성될 이미지 파일 이름
    )

    if output_drawing_path:
        print(f"변환된 이미지가 '{output_drawing_path}'에 저장되었습니다.")
        # (선택 사항) 변환된 더미 이미지를 바로 확인
        # try:
        #     Image.open(output_drawing_path).show()
        # except Exception as e:
        #     print(f"변환된 이미지 표시 중 오류 발생: {e}")
    else:
        print("이미지 변환에 실패했습니다. API 키 설정 및 네트워크 연결을 확인하세요.")
else:
    print("더미 입력 이미지를 준비할 수 없어 Drawing 모듈 테스트를 건너뜝니다.")


# --- 2. Chatbot 모듈 테스트 (텍스트) ---
print("\n--- Chatbot 모듈 테스트 (텍스트) ---")
user_text_question = input("💬 AI 챗봇에게 텍스트로 질문하세요 (예: 오늘 날씨 어때?): ")

# AI-Tools 라이브러리 chatbot 모듈 호출 (텍스트 전용)
text_response = ai_tools.chatbot.ask_text(user_text_question)

if text_response:
    print(f"AI 챗봇 답변: {text_response}")
else:
    print("AI 챗봇 답변을 받지 못했습니다. Gemini API 키 설정 및 네트워크 연결을 확인하세요.")

# --- 3. Chatbot 모듈 테스트 (멀티모달 - 이미지+텍스트) ---
print("\n--- Chatbot 모듈 테스트 (멀티모달 - 이미지+텍스트) ---")
dummy_input_image_path_vision = "test_input_image_for_vision.png"
try:
    Image.new('RGB', (300, 200), color = 'yellow').save(dummy_input_image_path_vision)
    print(f"더미 비전 입력 이미지 생성: {dummy_input_image_path_vision}")
except Exception as e:
    print(f"오류: 더미 비전 이미지 생성 실패: {e}")
    dummy_input_image_path_vision = None # 이미지 생성 실패 시 None으로 설정

if dummy_input_image_path_vision:
    user_vision_question = input(f"🖼️✨ {dummy_input_image_path_vision} 이미지에 대해 AI 챗봇에게 질문하세요 (예: 이 이미지는 무엇을 보여주나요?): ")

    # AI-Tools 라이브러리 chatbot 모듈 호출 (멀티모달)
    vision_response = ai_tools.chatbot.ask_vision(
        image_path=dummy_input_image_path_vision,
        question=user_vision_question
    )

    if vision_response:
        print(f"AI 챗봇 (비전) 답변: {vision_response}")
    else:
        print("AI 챗봇 (비전) 답변을 받지 못했습니다. Gemini API 키 설정 및 네트워크 연결을 확인하세요.")
else:
    print("더미 비전 입력 이미지를 준비할 수 없어 멀티모달 챗봇 테스트를 건너뜝니다.")

print("\n--- AI-Tools 라이브러리 통합 테스트 완료 ---")