from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from tts import speak

app = FastAPI()

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
