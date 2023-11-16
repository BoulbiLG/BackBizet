from flask import Blueprint, jsonify, request, Flask
from flask_pymongo import PyMongo
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/Bizeterie?retryWrites=true&w=majority')
app = Flask(__name__)

envoieCommentaire = Blueprint('envoieCommentaire', __name__)

@envoieCommentaire.route('/envoieCommentaire', methods=['POST'])
def envoieCommentaire_def():
    db = client['Bizeterie']
    collection = db['commentaire']

    data = request.json
    identifiant = request.args.get('identifiant', None)
    pseudo = request.args.get('pseudo', None)
    commentaire = request.args.get('commentaire', None)

    print('identifiant : ', identifiant)
    print('pseudo : ', pseudo)
    print('commentaire : ', commentaire)

    date_du_jour = datetime.now()

    mois_fr = {
        1: "janvier", 2: "février", 3: "mars", 4: "avril",
        5: "mai", 6: "juin", 7: "juillet", 8: "août",
        9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
    }

    date_formatee = date_du_jour.strftime("%d ") + mois_fr[date_du_jour.month] + date_du_jour.strftime(" %Y")

    print('date_formatee : ', date_formatee)

    data = {
        "date": date_formatee,
        "identifiant": identifiant,
        "pseudo": pseudo,
        "commentaire": commentaire,
    }
    try:
        collection.insert_one(data)

        return jsonify({"message": "like ajouté !"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
