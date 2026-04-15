from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def process_text(text):
    prompt = f"""
You are an AI agent.

Extract:
1. intent (create_file, write_code, summarize, chat)
2. filename (if user wants to save output)
3. code (if needed)
4. save (true/false → whether user wants to save output)

Rules:
- "Summarize this and save to summary.txt" →
  intent = summarize
  filename = summary.txt
  save = true

- "Write python code and save to test.py" →
  intent = write_code
  filename = test.py
  save = true

- If no save instruction → save = false

Return ONLY JSON:

{{
  "intent": "...",
  "filename": "...",
  "code": "...",
  "save": true/false
}}

Text: {text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()