import os
from groq import Groq

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

OUTPUT_DIR = "output"

# Ensure folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_file(filename):
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w") as f:
        f.write("")

    return {
        "message": f"File '{filename}' created.",
        "file_path": path,
        "content": ""
    }


def write_code(filename, code):
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w") as f:
        f.write(code)

    return {
        "message": f"Code written to '{filename}'.",
        "file_path": path,
        "content": code
    }


def summarize_text(text):
    prompt = f"""
Explain clearly in simple terms:

{text}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return {
        "message": "Summary generated",
        "file_path": None,
        "content": response.choices[0].message.content
    }