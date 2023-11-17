import sys
from webbrowser import register
from pymongo import MongoClient
import requests
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content, Accept, Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
    return response

app.after_request(after_request)

app.debug = False
CORS(app, resources={r"*": {"origins": "*"}})


# compte
from routes.compte.login import setup_login_routes
from routes.compte.signup import setup_signup_route

# contact
from routes.contact.mailEnvoie import mailEnvoie

# notification
from routes.notification.notification import notification

# user
from routes.user.like import like
from routes.user.envoieCommentaire import envoieCommentaire
from routes.user.recuperationCommentaire import recuperationCommentaire

# a la une Recherche
from routes.alaUne.recuperationMusiqueAlaUne import recuperationMusiqueAlaUne
from routes.alaUne.recuperationMusiqueLien import recuperationMusiqueLien
from routes.alaUne.recuperationMusiqueInfo import recuperationMusiqueInfo

# musique recherche
from routes.recherche.recuperationMusiqueAlaUne import recuperationMusiqueRecherche
from routes.recherche.recuperationMusiqueLien import recuperationMusiqueLienRecherche
from routes.recherche.recuperationMusiqueInfo import recuperationMusiqueInfoRecherche


#=========================================== INITIALISATION DU SERVEUR TERMINE ===============================================#


# compte
app.register_blueprint(setup_signup_route(app))
app.register_blueprint(setup_login_routes(app))

# mailEnvoie
app.register_blueprint(mailEnvoie)

# notification
app.register_blueprint(notification)

# compte
app.register_blueprint(like)
app.register_blueprint(envoieCommentaire)
app.register_blueprint(recuperationCommentaire)

# a la une
app.register_blueprint(recuperationMusiqueAlaUne)
app.register_blueprint(recuperationMusiqueLien)
app.register_blueprint(recuperationMusiqueInfo)

# musique recherche
app.register_blueprint(recuperationMusiqueRecherche)
app.register_blueprint(recuperationMusiqueLienRecherche)
app.register_blueprint(recuperationMusiqueInfoRecherche)



#===========================================LANCEMENT DU SERVER===============================================#
if __name__ == '__main__':
    url = "mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(url, connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
    collection = client.db["things"]
    app.run(host='0.0.0.0', port=1234)