from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def process_text(text):
    prompt = f"""
You are an AI agent that converts user commands into structured JSON.

IMPORTANT RULES:
- Always return valid JSON only
- Do NOT return explanations
- Do NOT return markdown
- Generate REAL working code when asked

INTENTS:
1. create_file → when user wants to create a file
2. write_code → when user asks for code
3. summarize → when user asks explanation
4. chat → normal conversation

RULES FOR write_code:
- ALWAYS generate FULL working code
- NEVER return just "cpp" or "python"
- If language is CPP → generate complete C++ program
- If filename not provided → generate default filename

DEFAULT FILENAMES:
- cpp → code.cpp
- python → code.py

OUTPUT FORMAT:
{{
  "intent": "...",
  "filename": "...",
  "code": "...",
  "save": true
}}

USER INPUT:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content