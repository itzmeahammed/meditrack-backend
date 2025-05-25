import openai
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

medicine_ai_bp = Blueprint('medicine_ai', __name__)
openai.api_key = os.getenv("OPEN_AI_API_KEY")

@medicine_ai_bp.route('/ask_medicine', methods=['POST', 'OPTIONS'])
def ask_medicine():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"message": "No query provided."}), 400

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a medical assistant. Only answer about medicines. "
                        "If someone asks about a medicine, respond with simple information: "
                        "1. What it is used for, and 2. Important notes if any. "
                        "Do not answer unrelated questions. Be short and direct."
                    )
                },
                {
                    "role": "user",
                    "content": f"Tell me about {query}. Provide uses and important information."
                }
            ],
            max_tokens=200,
            temperature=0.3,
        )

        result = response.choices[0].message.content.strip()

        return jsonify({"answer": result}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
