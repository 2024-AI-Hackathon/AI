from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def fix_text(stt_result: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "텍스트 오류를 수정합니다."},
            {"role": "user", "content": stt_result},
        ]
    )
    return response.choices[0].message.content.strip()
