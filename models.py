# models.py
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

def create_user(email, password, username, role, mobile):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        "email": email,
        "password": hashed_password,
        "username": username,
        "role": role,
        "mobile": mobile
    }
    return user

def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def get_product_by_id(product_id):
    return mongo.db.products.find_one({"_id": product_id})

def get_all_products():
    return mongo.db.products.find()

def create_product(product_name, price, stock, description, category):
    product = {
        "productName": product_name,
        "price": price,
        "stock": stock,
        "description": description,
        "category": category
    }
    return product