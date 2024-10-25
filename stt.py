import speech_recognition as sr

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = r.listen(source)
        said = ""

        try:
            # 한국어 인식
            said = r.recognize_google(audio, language="ko-KR")
            return {"text": said}
        except sr.UnknownValueError:
            return {"error": "Could not understand audio"}
        except sr.RequestError as e:
            return {"error": f"API request failed: {e}"}
