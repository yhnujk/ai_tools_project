# 🎨 AI-Tools: 당신의 게임과 앱에 생명을 불어넣는 AI 모듈 라이브러리 🚀

---

### ✨ 프로젝트 소개

AI-Tools는 **인공지능의 강력한 기능을 당신의 애플리케이션에 손쉽게 통합하고 맞춤화할 수 있도록 돕는 혁신적인 파이썬 라이브러리**입니다. ... (이 부분은 당신의 아이디어를 자세히 설명하면 좋습니다.)

### 🚀 주요 기능

- **그림체 변환 (Drawing Module):** AI를 활용하여 2D 이미지의 스타일을 원하는 대로 변환합니다. (예: 사진을 만화체로, 스케치를 유화로)
- **대화형 챗봇 (Chatbot Module):** AI 챗봇을 애플리케이션에 통합하여 자연어 기반의 대화 기능을 제공합니다. (텍스트, 멀티모달 지원)

### 🛠️ 개발 환경 및 사용법

1. **환경 설정:**
   - Python 3.8 이상
   - `pip install Pillow requests openai google-generativeai python-dotenv`

2. **API 키 설정:**
   - 프로젝트 루트에 `.env` 파일을 생성하고 다음 형식으로 API 키를 저장합니다:
     ```
     OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
     GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
     ```

3. **사용 예시:**
   ```python
   import ai_tools.drawing
   import ai_tools.chatbot
   import os
   from PIL import Image

   # .env 파일에서 환경 변수 로드
   from dotenv import load_dotenv
   load_dotenv()

   # 그림체 변환 예시
   # (테스트를 위해 실제 이미지 경로로 변경하거나, dummy_input_image.png 파일을 만들어 사용하세요)
   # Image.new('RGB', (200, 200), color = 'red').save("dummy_input_image.png")
   # transformed_image_path = ai_tools.drawing.draw(
   #     image_path="dummy_input_image.png",
   #     style_prompt=input("원하는 그림체 스타일을 입력하세요: ")
   # )
   # if transformed_image_path:
   #     print(f"변환된 이미지가 '{transformed_image_path}'에 저장되었습니다.")

   # 텍스트 챗봇 예시
   # user_question = input("AI 챗봇에게 질문하세요: ")
   # chat_response = ai_tools.chatbot.ask_text(user_question)
   # if chat_response:
   #     print(f"AI 챗봇 답변: {chat_response}")
   ```

### 💡 기여 및 라이선스

... (추후 추가)