import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# 🔐 MongoDB URI from environment (Render / Atlas)
app.config["MONGO_URI"] = os.environ.get(
    "MONGO_URI",
    "mongodb://localhost:27017/authdb"  # local fallback
)

mongo = PyMongo(app)
users = mongo.db.users


# ✅ ROOT HEALTH CHECK
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server is running"}), 200


# ✅ SIGNUP
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Invalid request"}), 400

    email = data["email"]
    password = data["password"]

    if users.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 409

    users.insert_one({
        "email": email,
        "password": generate_password_hash(password)
    })

    return jsonify({"message": "Signup successful"}), 201


# ✅ LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Invalid request"}), 400

    email = data["email"]
    password = data["password"]

    user = users.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful"}), 200


# ❌ DO NOT RUN app.run() ON RENDER
# Gunicorn will start the app
