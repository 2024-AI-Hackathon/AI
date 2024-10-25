from fastapi import FastAPI
from stt import get_audio
from tts import speak

app = FastAPI()

# 엔드포인트를 통해서만 get_audio가 호출되도록 설정
@app.get("/stt/")
async def speech_to_text():
    return get_audio()

@app.get("/tts/")
async def text_to_speech(text: str):
    return speak(text, save_path="voice.mp3")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)