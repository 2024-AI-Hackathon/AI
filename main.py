from urllib.request import Request
from fastapi import Request, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import json
from stt import get_audio
from tts import speak
from openai_utils import fix_text, translate_text
from pydub import AudioSegment

# ffmpeg 경로 설정
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"

app = FastAPI()
                                                                                            
# CORS 설정
origins = ["http://localhost:5173", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STT 엔드포인트
@app.get("/stt")
async def stt():
    try:
        return get_audio()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# STT 웹소켓 엔드포인트
@app.websocket("/ws/stt")
async def websocket_speech_to_text(websocket: WebSocket):
    await websocket.accept()
    listening = False
    try:
        while True:
            message = await websocket.receive_text()
            if message == "start" and not listening:
                listening = True
                await websocket.send_text("Listening started...")
                while listening:
                    result = get_audio()
                    await websocket.send_text(json.dumps(result, ensure_ascii=False))
                    await asyncio.sleep(1)
            elif message == "stop":
                listening = False
                await websocket.send_text("Listening stopped...")
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")

# TTS 웹소켓 엔드포인트
@app.websocket("/ws/tts")
async def websocket_tts(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            speak(data, save_path="voice.mp3")
            await websocket.send_text(f"Received and spoken: {data}")
    except WebSocketDisconnect:
        print("WebSocket connection closed")

# 텍스트 교정 엔드포인트
@app.post("/fix")
async def correct_text(input_data: dict):
    try:
        text = input_data.get("text")
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")
        corrected_text = fix_text(text)
        return {"original": text, "corrected": corrected_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 번역 엔드포인트
@app.post("/translate")
async def translate(request: Request):
    data = await request.json()
    text = data.get("text")
    target_lang = data.get("target", "en")

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    translated_text = translate_text(text, target_lang).strip('\"')
    return {"original": text, "translated": translated_text}
