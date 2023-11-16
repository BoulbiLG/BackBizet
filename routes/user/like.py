from flask import Blueprint, jsonify, request, Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/Bizeterie?retryWrites=true&w=majority')
app = Flask(__name__)

like = Blueprint('like', __name__)

@like.route('/like', methods=['POST'])
def like_def():
    db = client['Bizeterie']
    collection = db['musiqueInfo']

    data = request.json
    like = data.get('like')
    identifiant = data.get('identifiant')

    likeNumber = int(like)
    likeTotal = likeNumber + 1

    try:
        collection.update_one(
            {'identifiant': identifiant},
            {'$set': {'like': likeTotal}}
        )

        return jsonify({"message": "like ajouté !"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
