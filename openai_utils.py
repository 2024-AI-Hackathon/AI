from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 텍스트 오류 수정 메서드
def fix_text(stt_result: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "텍스트 오류를 수정합니다."},
            {"role": "user", "content": stt_result},
        ]
    )
    return response.choices[0].message.content.strip()

# 텍스트 언어 번역 메서드
def translate_text(text: str, target_lang: str) -> str:
    prompt = (
        f"다음 텍스트를 {target_lang}로 번역해 주세요:\n"
        f"\"{text}\""
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 유용한 번역 도우미입니다."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content.strip()