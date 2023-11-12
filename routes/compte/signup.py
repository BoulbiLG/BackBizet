from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
import bcrypt

signup_blueprint = Blueprint('signup', __name__)

def setup_signup_route(app):
    app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/Bizeterie?retryWrites=true&w=majority'
    mongo = PyMongo(app)

    @signup_blueprint.route('/signup', methods=['POST'])
    def signup():
        data = request.json
        username = data.get('pseudo')
        email = data.get('email')
        password = data.get('password')

        try:
            user = mongo.db.users.find_one({"email": email})
            if user:
                return jsonify({"message": "L'utilisateur existe déjà"}), 409

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            user_data = {
                "username": username,
                "email": email,
                "password": hashed_password
            }

            mongo.db.users.insert_one(user_data)

            return jsonify({"message": "Utilisateur créé avec succès !"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return signup_blueprint