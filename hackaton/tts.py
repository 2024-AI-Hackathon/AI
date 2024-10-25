from gtts import gTTS
# ModuleNotFoundError: No module named 'gtts'
# pip install gtts

import os
import playsound
# ModuleNotFoundError: No module named 'playsound'
# pip install playsound==1.2.2

#######################
# 3. 구글 TTS(텍스트->음성)
#######################

def speak(text):
    tts = gTTS(text=text, lang='ko') # 구글의 TTS클래스로 tts객체 생성(텍스트 -> 음성)
    filename='voice.mp3' # 파일명 지정
    tts.save(filename) # 파일 생성
    playsound.playsound(filename) # 해당 음성파일 실행
    os. remove (filename) # 파일 삭제

speak("만나서 반갑습니다.") # 함수 호출하여 텍스트를 음성으로 바꿔 줍니다.~