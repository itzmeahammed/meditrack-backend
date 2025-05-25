from flask import Blueprint, request, jsonify
from models import mongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('order', __name__)
product_bp = Blueprint('product', __name__)
import openai
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os


@order_bp.route('/place_order', methods=['POST'])
@jwt_required() 
def place_order():
    email = get_jwt_identity() 

    data = request.get_json()

    cart_items = data['cartItems']
    total_amount = data['totalAmount']
    billing_details = data['billingDetails']

    order_details = {
        "user_email": email,  
        "cart_items": cart_items,
        "total_amount": total_amount,
        "billing_details": billing_details,
        "status": "Order Placed", 
        "created_at": datetime.now(),
    }

    try:
        order = mongo.db.orders.insert_one(order_details)

        for item in cart_items:
            product_id = item['id']
            quantity = item['quantity']

            mongo.db.products.update_one(
                {"_id": ObjectId(product_id)},
                {"$inc": {"stock": -quantity}}
            )

        return jsonify({"message": "Order placed successfully!"}), 200

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@product_bp.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    product_name = data.get('productName')
    price = data.get('price')
    stock = data.get('stock')
    description = data.get('description')
    category = data.get('category')

    # Insert product into MongoDB
    product = {
        "productName": product_name,
        "price": price,
        "stock": stock,
        "description": description,
        "category": category
    }

    try:
        mongo.db.products.insert_one(product)
        return jsonify({"message": "Product added successfully!"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@product_bp.route('/view_products', methods=['GET'])
def view_products():
    try:
        products = mongo.db.products.find()
        products_list = [
            {"id": str(product["_id"]), "productName": product["productName"], "price": product["price"],
             "stock": product["stock"], "description": product["description"], "category": product["category"]}
            for product in products
        ]
        return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@product_bp.route('/edit_product/<product_id>', methods=['PUT'])
def edit_product(product_id):
    data = request.get_json()
    updated_product = {
        "productName": data.get("productName"),
        "price": data.get("price"),
        "stock": data.get("stock"),
        "description": data.get("description"),
        "category": data.get("category"),
    }

    try:
        # Make sure product_id is a valid ObjectId
        if not ObjectId.is_valid(product_id):
            return jsonify({"message": "Invalid product ID."}), 400

        result = mongo.db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": updated_product}
        )

        if result.matched_count:
            return jsonify({"message": "Product updated successfully!"}), 200
        else:
            return jsonify({"message": "Product not found."}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@product_bp.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        # Make sure product_id is a valid ObjectId
        if not ObjectId.is_valid(product_id):
            return jsonify({"message": "Invalid product ID."}), 400

        result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})

        if result.deleted_count:
            return jsonify({"message": "Product deleted successfully!"}), 200
        else:
            return jsonify({"message": "Product not found."}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

