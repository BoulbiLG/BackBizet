from flask import Blueprint, jsonify, request, current_app, Flask
import json

from bson import ObjectId
from dns.rdatatype import NULL
from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/Bizeterie?retryWrites=true&w=majority')
app = Flask(__name__)

recuperationMusiqueInfo = Blueprint('recuperationMusiqueInfo', __name__)

def json_serial(obj):
    try:
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TypeError("Type not serializable")
    except Exception as e:
        print("Error occurred during serialization:")
        print("Object:", obj)
        print("Error:", str(e))
        raise TypeError(f"Type not serializable: {obj}, Error: {str(e)}")

@recuperationMusiqueInfo.route('/recuperationMusiqueInfo', methods=['GET'])
def recuperationMusiqueInfo_def():

    db = client['Bizeterie']
    collection = db['musiqueInfo']

    identifiant = request.args.get('identifiant', None)

    query = {'$and': [{'identifiant': identifiant}]}

    try:
        data = list(collection.find(query))


        # ==================== RECUPERATION TRADES TERMINEE ==================== # maxProfit
        
        
        data = json.loads(json.dumps(data, default=json_serial))
        return jsonify({'data': data})

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors du renvoie des données", "details": str(e)}), 500
