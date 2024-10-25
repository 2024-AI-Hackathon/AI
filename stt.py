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
            print("Your speech:", said)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    
    return said

text = get_audio()
