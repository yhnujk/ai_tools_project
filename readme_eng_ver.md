# usingai: AI-Based Module Collection for Games & Applications

This package utilizes the **Google Gemini API** and **OpenAI DALL·E 3 API** to provide various AI-powered features for game and app development. Currently, it includes **image style transformation** and an **AI chatbot**.

만약 한글 버전을 원한다면, [이 곳을 눌러주세요](README.md)

---

## 🚀 Key Features

- **🖼️ Image Style Transformation**  
  Generate images in artistic styles (e.g., watercolor, pixel art, ink painting) based on a text prompt.

- **🤖 AI Chatbot**  
  A multimodal chatbot that can respond to text and image-based queries using the Gemini API.

---

## 📦 Installation

```bash
pip install usingai39  # For Ren'Py (Python 3.9)
pip install usingai311 # For modern Python (3.11+)
```

To download directly from PyPI:
```
https://pypi.org/project/usingai39/   # Optimized for Python 3.9 / Ren'Py
https://pypi.org/project/usingai311/  # Ideal for Python 3.11 and newer environments
```

---

## ⚙️ How to Use

### 1. Automatic API Key Setup

If the `.env` file is missing, it will be created on first run. 
You'll be prompted to enter your **OpenAI** and **Google Gemini** API keys.

Generate your API keys here:

- [Get your OpenAI API Key](https://platform.openai.com/account/api-keys)
- [Get your Google Gemini API Key](https://ai.google.dev/gemini-api/docs/get-started)

```bash
python -m ai_tools.main
```

Alternatively, you can directly run `main.py`, which will automatically invoke the key setup script.

---

### 2. Example Execution

After launch, the following menu will be shown:

```
💾 Enter the folder path to save generated images (press Enter to use the same folder as input image):

(Note: This path is fixed for the session!)

1. Image Style Transformation
2. AI Chatbot
3. Exit
```

---

## 🧪 Testing

You can run unit tests or try image generation using the following command:

```bash
python tests/test_ai_tools.py
```

---

## 🛠️ Development Checklist

📊 [View checklist.md](docs/checklist.md)

---

## 🤝 Contributions

This project is open-source and welcomes contributors!  
For details, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 📄 License

This project is distributed under the [MIT License](LICENSE).

---

## ⚠️ Usage Notice

- This project uses OpenAI and Google Gemini APIs. You must comply with their respective **usage policies**.
- The developer is not responsible for the generated content. Use at your own discretion.

📄 Read the full policies here: [OpenAI Usage Policy](https://openai.com/policies/usage-policies), [Gemini Terms](https://ai.google.dev/terms)
