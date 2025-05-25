import openai
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

analyze_bp = Blueprint('analyze', __name__)
openai.api_key = os.getenv("OPEN_AI_API_KEY")

@analyze_bp.route('/analyze_stock', methods=['POST', 'OPTIONS'])
def analyze_stock():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    data = request.get_json()
    products = data.get("products", [])

    if not products:
        return jsonify({"message": "No products provided."}), 400

    # Prepare product details
    product_details = "\n".join([f"{p['productName']}: {p['stock']} in stock" for p in products])

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an inventory assistant. long suggestions. Just point out which products are low and need restocking. tell about the stocks"
                },
                {
                    "role": "user",
                    "content": f"Analyze these products and tell me the product list the ones that need restocking (stock less than 50000):\n{product_details}"
                }
            ],
            max_tokens=150,
            temperature=0.2,
        )

        analysis_result = response.choices[0].message.content.strip()

        return jsonify({"analysisResult": analysis_result}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
