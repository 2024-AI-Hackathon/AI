from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import speech_recognition as sr
from pydub import AudioSegment
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import asyncio
import json
from stt import get_audio
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"  # 실제 ffmpeg 설치 경로를 설정
from fastapi.staticfiles import StaticFiles
from tts import speak

app = FastAPI()
# CORS 설정
origins = [
    "http://localhost:5173",  # 프론트엔드가 로컬에서 실행 중인 경우
    "http://127.0.0.1:3000",  # 추가 로컬 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/speech-to-text")
async def stt():
    return get_audio()

@app.websocket("/ws/speech-to-text/")
async def websocket_speech_to_text(websocket: WebSocket):
    await websocket.accept()
    listening = False  # 음성 인식 중인지 여부

    while True:
        try:
            # 클라이언트에서 메시지 수신
            message = await websocket.receive_text()

            if message == "start" and not listening:
                listening = True
                await websocket.send_text("Listening started...")
                
                # 음성 인식을 비동기로 수행
                # 음성 인식을 비동기로 수행
                while listening:
                    result = get_audio()  # 음성을 텍스트로 변환
                    await websocket.send_text(json.dumps(result, ensure_ascii=False))  # JSON 문자열로 변환하여 전송
                    await asyncio.sleep(1)  # 간격을 두고 반복

            elif message == "stop":
                listening = False
                await websocket.send_text("Listening stopped...")

        except WebSocketDisconnect:
            print("Client disconnected")
            break
        except Exception as e:
            await websocket.send_text("")
            break
# 정적 파일 제공 설정 (HTTP 요청 처리)
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

@app.websocket("/ws/tts")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            speak(data, save_path="voice.mp3")
            await websocket.send_text(f"Received and spoken: {data}")
    except WebSocketDisconnect:
        print("WebSocket connection closed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
