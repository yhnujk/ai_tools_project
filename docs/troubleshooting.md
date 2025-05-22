# 트러블슈팅 기록 (Troubleshooting Log)

이 문서는 AI-Tools 프로젝트를 개발하고 실행하는 과정에서 마주쳤던 주요 문제점들과 이를 해결했던 과정을 기록합니다. 비슷한 문제를 겪는 다른 개발자들에게 도움이 되기를 바랍니다.

---

## 1. `FileNotFoundError` (경로 슬래시 문제)

-   **문제 발생:** Windows 환경에서 이미지 파일 경로를 입력할 때 백슬래시(`\`)를 사용했으나, Python 내부 또는 특정 라이브러리(예: `os.path.exists`)에서 일반 슬래시(`/`)를 예상하여 파일이 존재하지 않는다는 `FileNotFoundError`가 발생했습니다.
-   **원인 분석:** Windows 파일 시스템은 백슬래시와 슬래시를 모두 허용하지만, Python이나 웹 기반 환경에서는 슬래시가 더 보편적이며 일관성을 유지하는 것이 중요합니다. 특히 문자열 처리나 URL 생성 시 예상치 못한 오류를 유발할 수 있습니다.
-   **해결 방법:** `main.py`에서 사용자로부터 파일 경로를 입력받는 즉시, 모든 백슬래시를 일반 슬래시로 변환하도록 `input_image_path_raw.replace('\\', '/')` 코드를 추가했습니다.
    ```python
    # main.py
    input_image_path_raw = input("변환할 이미지 파일의 전체 경로를 입력하세요 (...): ")
    input_image_path = input_image_path_raw.replace('\\', '/') # 여기에 추가
    ```

---

## 2. `404 Gemini 1.0 Pro Vision has been deprecated` 오류 (Gemini 모델 버전 문제)

-   **문제 발생:** `_get_image_description_with_gemini` 함수에서 Google Gemini Vision API를 호출할 때 `gemini-pro-vision` 모델을 사용했습니다. 하지만 이 모델이 2024년 7월 12일부로 지원이 중단될 예정이며, 현재 시점에는 이미 사용이 제한되어 `404 Not Found` 오류가 발생했습니다.
-   **원인 분석:** 사용 중인 API 모델이 최신 버전으로 업데이트되지 않았거나, 서비스 제공자의 정책 변경으로 인해 더 이상 지원되지 않는 모델을 호출했기 때문입니다.
-   **해결 방법:** `ai_tools/drawing.py` 파일 내 `_get_image_description_with_gemini` 함수에서 Gemini 모델 이름을 `gemini-pro-vision` 대신 현재 사용 가능한 최신 Vision 모델인 **`gemini-1.5-flash`**로 변경했습니다.
    ```python
    # ai_tools/drawing.py
    model = genai.GenerativeModel('gemini-1.5-flash') # 모델 이름 변경
    ```

---

## 3. `IndentationError: unexpected indent` (들여쓰기 오류)

-   **문제 발생:** 코드 수정 및 복사-붙여넣기 과정에서 `ai_tools/drawing.py` 파일의 특정 코드 블록, 특히 DALL-E 프롬프트 생성 부분에서 파이썬의 **들여쓰기(Indentation)** 규칙이 어긋나 `IndentationError`가 발생했습니다. 파이썬은 들여쓰기를 통해 코드 블록의 시작과 끝을 구분하므로, 공백 개수가 일치하지 않으면 문법 오류로 간주합니다.
-   **원인 분석:** 주로 텍스트 에디터의 설정 문제(탭과 공백 혼용)나, 수동 복사-붙여넣기 시 들여쓰기가 깨지는 경우 발생합니다.
-   **해결 방법:** 문제가 발생한 줄의 들여쓰기를 수동으로 정확히 **4칸 공백**으로 맞춰 재정렬했습니다. VS Code와 같은 IDE는 들여쓰기 가이드를 제공하므로 이를 활용하여 일관성을 유지하는 것이 중요합니다.

---

## 4. `400 Client Error: Bad Request` (DALL-E 3 프롬프트 및 API 계정 문제)

이 문제는 가장 복합적이었으며, 여러 원인이 겹쳐 발생했습니다.

### 가. 프롬프트 내용/형식 문제

-   **문제 발생:** Gemini Vision API가 분석한 이미지 설명 텍스트가 OpenAI DALL-E 3가 이해하거나 선호하지 않는 부가적인 설명(예: "Here's a description...", "The image is...", "The image depicts...")을 포함하여 DALL-E 3 API가 `400 Bad Request`를 반환했습니다. DALL-E 3는 간결하고 직접적인 이미지 생성 지시 프롬프트를 선호합니다.
-   **해결 방법:** `ai_tools/drawing.py` 파일 내 `draw` 함수에서 `image_description`을 DALL-E 3 프롬프트로 변환하는 로직을 강화했습니다.
    1.  **불필요한 서두 제거:** `image_description.strip()` 외에도, Gemini가 자주 사용하는 다양한 서두 문구들(예: `"Here's a description..."`, `"The image is..."`, `"Description:"`)을 `startswith`와 `lower()`를 사용하여 유연하게 제거하도록 수정했습니다.
    2.  **프롬프트 길이 제한:** DALL-E 3가 너무 긴 프롬프트에 민감하게 반응할 수 있으므로, 프롬프트의 핵심 내용을 **200자 이내**로 제한하고, 단어 단위로 잘라내도록 로직을 개선했습니다.
    3.  **DALL-E 선호 형식 도입:** 프롬프트 시작을 `An artwork depicting:` 과 같이 DALL-E 3가 잘 이해하는 지시 형식으로 고정하여 명확성을 높였습니다. 또한, `Realistic photo quality, high detail.`과 같은 품질 지시어를 추가했습니다.

### 나. OpenAI API 계정 크레딧 부족

-   **문제 발생:** 프롬프트 정제를 최대로 강화했음에도 불구하고 `400 Bad Request` 오류가 지속되었습니다. 확인 결과, OpenAI DALL-E 3 API는 기본적으로 유료 서비스이며, 제 OpenAI 계정에 DALL-E 3 사용을 위한 **충분한 크레딧이 없었기 때문**에 API 호출이 거부되었습니다 (무료 티어만으로는 DALL-E 3 사용 불가).
-   **해결 방법:** OpenAI 플랫폼 웹사이트(`platform.openai.com`)에 접속하여 **결제 수단을 등록하고 최소 금액($10)**의 크레딧을 충전했습니다. 크레딧 충전 후 기존에 사용하던 API 키로 재시도하자 DALL-E 3 API 호출이 정상적으로 성공하고 이미지가 생성되었습니다. 이는 API 키의 유효성보다는 계정의 결제 상태가 문제였음을 명확히 해주었습니다.

---

## 결론

이러한 문제 해결 과정을 통해 API를 사용하는 개발에서는 단순히 코드의 문법적 정확성뿐만 아니라, **외부 서비스의 API 정책, 모델 버전 관리, 프롬프트 엔지니어링, 그리고 계정/결제 상태**와 같은 다양한 외부 요인들이 중요하게 작용한다는 것을 배울 수 있었습니다. 인내심을 가지고 각 단계를 디버깅하며 접근하는 것이 중요합니다.