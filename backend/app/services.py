# backend/app/services.py
import os, requests

OPENAI_API_KEY = os.getenv("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
ELEVEN_API_KEY = os.getenv("sk_fd61b1b4081cabaa4fb001f5eb88a36ce9ba14de23cea25b
ELEVEN_VOICE_ID = os.getenv("ys3XeJJA4ArWMhRpcX1D", "your_default_voice_id")

def call_openai_chat(user_text: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",   # change if needed
        "messages": [{"role": "user", "content": user_text}]
    }
    r = requests.post(url, json=payload, headers=headers, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def eleven_tts_bytes(text: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text}
    r = requests.post(url, json=payload, headers=headers, timeout=60)
    r.raise_for_status()
    return r.content
