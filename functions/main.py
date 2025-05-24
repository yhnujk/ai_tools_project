from firebase_functions import https_fn
from firebase_admin import initialize_app
import requests
import os

initialize_app()

@https_fn.on_request()
def hello_world(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("Hello from Firebase!")

@https_fn.on_request()
def stylize_image(req: https_fn.Request) -> https_fn.Response:
    data = req.get_json()
    prompt = data.get("prompt")
    user_api_key = req.headers.get("x-openai-key")

    if not prompt or not user_api_key:
        return https_fn.Response("Missing prompt or API key", status=400)

    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {user_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024"
            }
        )
        result = response.json()
        image_url = result["data"][0]["url"]
        return https_fn.Response(image_url)
    except Exception as e:
        return https_fn.Response(f"Error: {str(e)}", status=500)

@https_fn.on_request()
def chat_with_gemini(req: https_fn.Request) -> https_fn.Response:
    data = req.get_json()
    user_prompt = data.get("prompt")
    gemini_api_key = req.headers.get("x-gemini-key")

    if not user_prompt or not gemini_api_key:
        return https_fn.Response("Missing prompt or Gemini API key", status=400)

    try:
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}"
        response = requests.post(
            gemini_url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": user_prompt}]}]
            }
        )
        result = response.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
        return https_fn.Response(reply)
    except Exception as e:
        return https_fn.Response(f"Error: {str(e)}", status=500)
