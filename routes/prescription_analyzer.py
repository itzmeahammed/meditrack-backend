import os
import openai
import easyocr
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

prescription_bp = Blueprint('prescription_analyzer', __name__)
openai.api_key = os.getenv("OPEN_AI_API_KEY")

# Set upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize OCR reader
reader = easyocr.Reader(['en'])

@prescription_bp.route('/analyze_prescription', methods=['POST'])
def analyze_prescription():
    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400

    # Save the uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # OCR: Extract text from image
        result = reader.readtext(file_path, detail=0)
        extracted_text = " ".join(result)

        if not extracted_text:
            return jsonify({"message": "No text found in the prescription."}), 400

        # Send extracted text to OpenAI for medicine name cleaning
        ai_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant specialized in reading prescriptions. "
                        "Given raw text from a doctor's handwriting, identify and list only the medicine names clearly. "
                        "Do not include other information."
                    )
                },
                {
                    "role": "user",
                    "content": f"Extract only the medicine names from this text:\n{extracted_text}"
                }
            ],
            max_tokens=200,
            temperature=0.3,
        )

        medicines = ai_response.choices[0].message.content.strip()

        return jsonify({"medicines": medicines}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
