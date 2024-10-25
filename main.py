from fastapi import FastAPI
from stt import get_audio

app = FastAPI()

# 엔드포인트를 통해서만 get_audio가 호출되도록 설정
@app.get("/speech-to-text/")
async def speech_to_text():
    return get_audio()