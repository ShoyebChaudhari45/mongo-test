from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/authdb"
mongo = PyMongo(app)
users = mongo.db.users

# ✅ ROOT TEST ROUTE
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server is running"}), 200

# ✅ LOGIN ROUTE (THIS WAS MISSING)
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email})
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    if bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


# ✅ SIGNUP ROUTE
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if users.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    users.insert_one({
        "email": email,
        "password": hashed_pw
    })

    return jsonify({"message": "Signup successful"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
