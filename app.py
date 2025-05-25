# app.py
from flask import Flask
from flask_cors import CORS
from config import Config
from models import mongo, bcrypt
from routes.auth import auth_bp
from routes.product import product_bp
from routes.analyze import analyze_bp 
from routes.medicine_ai import medicine_ai_bp
from routes.prescription_analyzer import prescription_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

# CORS(app, origins="http://localhost:3000", supports_credentials=True) 
# Initialize Extensions
mongo.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(analyze_bp, url_prefix='/analyze')   
app.register_blueprint(medicine_ai_bp, url_prefix='/medicine_ai')
app.register_blueprint(prescription_bp, url_prefix='/prescription')

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
