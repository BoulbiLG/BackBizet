from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
import bcrypt
import jwt
from bson import ObjectId

login_blueprint = Blueprint('login', __name__)

def setup_login_routes(app):
    @login_blueprint.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('email')
        password = data.get('password')

        try:
            app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/Bizeterie?retryWrites=true&w=majority'
            mongo = PyMongo(app)

            user = mongo.db.users.find_one({"username": username})
            if not user:
                return jsonify({"message": "Paire login/mot de passe incorrecte"}), 401

            hashed_password = user['password']
            entered_password_encoded = password.encode('utf-8')

            if bcrypt.checkpw(entered_password_encoded, hashed_password):
                user_data = {key: str(value) for key, value in user.items() if key != 'password'}

                token = jwt.encode({"userId": str(user['_id'])}, 'RANDOM_TOKEN_SECRET', algorithm='HS256')
                
                response_data = {"userId": str(user['_id']), "token": token, "user_data": user_data}
                return jsonify(response_data), 200
            else:
                return jsonify({"message": "Paire login/mot de passe incorrecte"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return login_blueprint