markdown
# AI-Tools: AI 기반 게임/앱 모듈 컬렉션

이 프로젝트는 **Google Gemini Vision API**와 **OpenAI DALL·E 3 API**를 활용하여 게임 및 애플리케이션 개발에 활용할 수 있는 다양한 AI 기반 도구(모듈)들을 제공합니다.  
현재 **이미지 스타일 변환** 및 **AI 챗봇** 기능을 포함하고 있습니다.

---

## 🚀 기능 (Features)

- **🖼️ 이미지 스타일 변환 (Drawing):**  
  주어진 이미지를 **Google Gemini Vision**으로 분석하고, **OpenAI DALL·E 3**를 사용하여 텍스트 프롬프트에 지정된 다양한 예술적 스타일(예: 유화, 픽셀아트, 수묵화 등)로 변환합니다.

- **🤖 AI 챗봇 (Chatbot):**  
  텍스트 기반 질문에 답변하거나, 이미지와 텍스트를 결합한 **멀티모달 질문**에 응답할 수 있습니다. (주로 Gemini API 활용)

---

## ⚙️ 설치 및 사용법 (Installation & Usage)

### 1. 프로젝트 클론 (Clone the Repository)

```bash
git clone https://github.com/yhnujk/ai_tools_project.git
cd ai_tools_project
```

### 2. 가상 환경 설정 (Virtual Environment Setup)

안정적인 개발 환경을 위해 **가상 환경 사용을 권장**합니다.

가상 환경 생성:

```bash
python -m venv .venv
```

가상 환경 활성화:

- **Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

- **macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. 의존성 설치 (Install Dependencies)

```bash
pip install -e .
# 또는
pip install python-dotenv openai google-generativeai requests Pillow
```

### 4. API 키 설정 (API Key Configuration)

프로젝트 루트 디렉토리(`ai_tools_project/`)에 `.env` 파일을 생성하고 아래 형식으로 API 키를 입력합니다:

```env
OPENAI_API_KEY="sk-YOUR_OPENAI_API_KEY_HERE"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

- `YOUR_OPENAI_API_KEY_HERE`는 [OpenAI Platform](https://platform.openai.com/)에서 발급받은 키로 교체하세요. (DALL·E 3 사용 시 유료 크레딧 필요)
- `YOUR_GEMINI_API_KEY_HERE`는 [Google AI Studio](https://makersuite.google.com/) 또는 [Google Cloud Console](https://console.cloud.google.com/)에서 발급받은 키로 교체하세요.

### 5. 프로젝트 실행 (Run the Project)

```bash
python main.py
```

실행 후, 아래와 같은 입력을 요청받습니다:

```
변환할 이미지 파일의 전체 경로를 입력하세요: C:\Users\YourName\Pictures\my_photo.jpg
원하는 이미지 스타일을 입력하세요: oil painting
```

생성된 이미지는 `output_파일명_스타일.png` 형식으로 저장됩니다.

### 6. 테스트 스크립트 실행 (Optional: Run Test Script)

```bash
python test_ai_tools.py
```

---

## 🛠️ 트러블슈팅 기록 (Troubleshooting Log)

개발 및 실행 과정에서 발생할 수 있는 문제와 해결 방법은 [`docs/troubleshooting.md`](docs/troubleshooting.md) 파일을 참조하세요.  
(API 키 오류, 모델 버전 문제, 프롬프트 포맷 등 유용한 정보 포함)

---

## 🤝 기여 (Contributing)

이 프로젝트는 오픈 소스로 개발되고 있습니다.  
기여 방법에 대한 자세한 내용은 [`CONTRIBUTING.md`](CONTRIBUTING.md)를 확인해주세요.

---

## 📄 라이선스 (License)

이 프로젝트는 [MIT License](LICENSE)에 따라 배포됩니다.
```
