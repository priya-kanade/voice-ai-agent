import json
import os
import re
from groq import Groq
from modules.llm import process_text
from modules.tools import create_file, write_code, summarize_text

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------- CHAT RESPONSE ----------------
def chat_response(text):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": text}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


# ---------------- MAIN AGENT ----------------
def run_agent(text):
    llm_output = process_text(text)

    print("RAW LLM RESPONSE:", llm_output)

    # ---------------- PARSE JSON ----------------
    try:
        json_match = re.search(r"\{.*\}", llm_output, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found")

        data = json.loads(json_match.group())

    except:
        return "chat", {
            "message": "Fallback to chat (parsing failed)",
            "file_path": None,
            "content": chat_response(text)
        }

    intent = data.get("intent", "chat")
    filename = data.get("filename")
    code = data.get("code", "")
    save_flag = data.get("save", False)
    summary_text = data.get("text", "")

    # ---------------- VALID INTENT ----------------
    valid_intents = ["create_file", "write_code", "summarize", "chat"]

    if intent not in valid_intents:
        return "chat", {
            "message": "Unrecognized intent → fallback to chat",
            "file_path": None,
            "content": chat_response(text)
        }

    # ---------------- FIX FILENAME ----------------
    if not filename or filename == "null":
        if intent == "write_code":
            if "cpp" in text.lower() or "c++" in text.lower():
                filename = "code.cpp"
            elif "python" in text.lower():
                filename = "code.py"
            else:
                filename = "code.txt"
        elif intent == "summarize":
            filename = "summary.txt"
        else:
            filename = "output.txt"

    filename = filename.replace(" ", "_")

    # ---------------- ACTIONS ----------------

    # ✅ CREATE FILE
    if intent == "create_file":
        return intent, create_file(filename)

    # ✅ WRITE CODE
# ✅ WRITE CODE
    elif intent == "write_code":

    # 🔥 STRONG VALIDATION (fixes your issue)
        invalid_code_outputs = ["cpp", "python", "code", "c++"]

        if (
            not code
            or code.strip().lower() in invalid_code_outputs
            or len(code.strip()) < 20
       ):
            code = chat_response(
                f"Write complete working {text}. Only output code. No explanation."
            )

    # 🔥 Ensure filename
        if not filename:
            if "cpp" in text.lower() or "c++" in text.lower():
                filename = "code.cpp"
            elif "python" in text.lower():
                filename = "code.py"
            else:
                filename = "code.txt"
    
        result = write_code(filename, code)
        return intent, result
    # ✅ SUMMARIZE (WITH COMPOUND SUPPORT)
    elif intent == "summarize":

        # Use LLM summary if available
        if summary_text:
            summary_result = {
                "message": "Summary generated",
                "file_path": None,
                "content": summary_text
            }
        else:
            summary_result = summarize_text(text)

        # 🔥 COMPOUND COMMAND: SAVE SUMMARY
        if save_flag:
            write_result = write_code(filename, summary_result["content"])

            return intent, {
                "message": f"Summary generated and saved to '{filename}'",
                "file_path": write_result["file_path"],
                "content": summary_result["content"]
            }

        return intent, summary_result

    # ✅ CHAT
    else:
        return intent, {
            "message": "Chat response generated",
            "file_path": None,
            "content": chat_response(text)
        }
        