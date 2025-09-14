# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
from .services import call_openai_chat, eleven_tts_bytes

app = FastAPI()

class AskIn(BaseModel):
    text: str

@app.post("/ask")
async def ask(payload: AskIn):
    try:
        reply_text = call_openai_chat(payload.text)
        audio_bytes = eleven_tts_bytes(reply_text)
        # Return base64 audio plus text (small demo). In production, upload the audio to storage and return a URL.
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        return {"text": reply_text, "audio_b64": audio_b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
