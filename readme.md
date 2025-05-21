# AI-Tools: AI 기반 게임/앱 모듈 컬렉션

이 프로젝트는 게임 및 애플리케이션 개발에 활용할 수 있는 다양한 AI 기반 도구(모듈)들을 제공합니다. 현재 이미지 스타일 변환 및 챗봇 기능을 포함하고 있습니다.

## 🚀 기능

* **이미지 스타일 변환 (Drawing):** 주어진 이미지와 텍스트 프롬프트를 사용하여 다양한 예술적 스타일로 이미지를 변환합니다. (예: 유화, 픽셀아트, 수묵화)
* **AI 챗봇 (Chatbot):** 텍스트 기반 질문에 답변하거나, 이미지와 텍스트를 결합한 멀티모달 질문에 응답할 수 있습니다.

## ⚙️ 설치 및 사용법

1.  **프로젝트 클론 (Clone the Repository):**
    ```bash
    git clone [https://github.com/yhnujk/ai_tools_project.git](https://github.com/yhnujk/ai_tools_project.git)
    cd ai_tools_project
    ```

2.  **가상 환경 설정 (Virtual Environment Setup):**
    * **가상 환경 생성:**
        ```bash
        python -m venv .venv
        ```
    * **가상 환경 활성화:**
        * Windows PowerShell:
            ```powershell
            .\.venv\Scripts\Activate.ps1
            ```
        * macOS / Linux:
            ```bash
            source ./.venv/bin/activate
            ```

3.  **의존성 설치 (Install Dependencies):**
    * `setup.py`에 정의된 모든 필수 라이브러리를 설치합니다.
    ```bash
    pip install -e .
    ```

4.  **API 키 설정 (API Key Configuration):**
    * **API 키 발급처:**
        * **Google Gemini API:** [Google AI Studio](https://aistudio.google.com/app/apikey) 또는 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
            * **`Create API Key`** 버튼을 클릭하여 키를 발급받으세요.
        * **OpenAI API (DALL-E):** [OpenAI Platform](https://platform.openai.com/api-keys)
            * **`Create new secret key`** 버튼을 클릭하여 키를 발급받으세요.

    * **`.env` 파일 생성:**
        프로젝트 루트 디렉토리 (`ai_tools_project/`)에 `.env`라는 이름의 파일을 생성하고 발급받은 API 키를 다음 형식으로 저장합니다.

        ```
        # .env 파일 내용
        OPENAI_API_KEY="sk-YOUR_OPENAI_API_KEY_HERE"
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
        ```
        `YOUR_OPENAI_API_KEY_HERE`를 OpenAI API 키로, `YOUR_GEMINI_API_KEY_HERE`를 Google Gemini Api에서 발급받은 키로 교체하세요.

5.  **테스트 스크립트 실행 (Run Test Script):**
    * 모든 설정이 완료되면, 다음 명령어로 라이브러리 기능을 테스트할 수 있습니다.
    ```bash
    python test_ai_tools.py
    ```
    이 스크립트는 이미지 변환 및 챗봇 기능을 시연합니다.

## 🤝 기여 (Contributing)

이 프로젝트는 오픈 소스로 개발될 예정입니다. 기여에 대한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md) 파일을 참고해주세요.

## 📄 라이선스 (License)

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.