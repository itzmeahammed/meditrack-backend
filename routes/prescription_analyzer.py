import os
import openai
import easyocr
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

prescription_bp = Blueprint('prescription_analyzer', __name__)
openai.api_key = os.getenv("OPEN_AI_API_KEY")

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'])

@prescription_bp.route('/analyze_prescription', methods=['POST'])
def analyze_prescription():
    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # OCR extract
        result = reader.readtext(file_path, detail=0)
        extracted_text = " ".join(result)

        if not extracted_text:
            return jsonify({"message": "No text found in the prescription."}), 400

        # AI request for medicine names + uses
        ai_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that reads prescriptions and explains medicines. "
                        "Given raw OCR text, return a JSON array with each medicine's name and its primary use. "
                        "Format strictly as: "
                        "[{\"name\": \"MedicineName\", \"use\": \"What it's used for\"}, ...] "
                        "Do not include anything else."
                    )
                },
                {
                    "role": "user",
                    "content": f"Extract medicine names and their uses from this text:\n{extracted_text}"
                }
            ],
            max_tokens=300,
            temperature=0.3,
        )

        medicines_json = ai_response.choices[0].message.content.strip()

        return jsonify({"medicines": medicines_json}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
