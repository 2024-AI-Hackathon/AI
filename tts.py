import os
from gtts import gTTS
import pygame

def speak(text, save_path="voice.mp3"):
    tts = gTTS(text=text, lang='ko')
    tts.save(save_path)

    pygame.mixer.init()
    pygame.mixer.music.load(save_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    os.remove(save_path)
