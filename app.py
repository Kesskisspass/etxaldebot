from flask import Flask, render_template, request, redirect
from modules.chatbot import get_response
from modules.db import get_produits_from_cat, get_producteurs_from_product, get_producteur_from_id
from modules.recommandation import get_reco
from flask import jsonify, make_response

app = Flask(__name__)

user = {'localisation':'','contexte':''}

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/send_message', methods=['POST'])
def create_entry():
    req = request.get_json()
    return get_response(req,user)

@app.route('/recommandation')
def recommandation():
    return render_template("recommandation.html")

@app.route('/send_recommandation', methods=['POST'])
def create_reco():
    req = request.get_json()
    liste = get_reco(req)
    res = make_response(jsonify(liste), 200)
    return res

@app.route('/get_product', methods=['POST'])
def fill_product():
    cat_id = request.get_json()
    print(cat_id)
    liste = get_produits_from_cat(cat_id['categorie'])
    print("debug",liste)
    res = make_response(jsonify(liste), 200)
    return res

@app.route('/get_producteurs', methods=['POST'])
def send_producteurs():
    prod = request.get_json()
    liste = get_producteurs_from_product(prod['id'])
    res = make_response(jsonify(liste), 200)
    return res

@app.route('/get_fiche_producteur', methods=['POST'])
def send_producteur():
    producteur = request.get_json()
    fiche = get_producteur_from_id(producteur['id'])
    res = make_response(jsonify(fiche), 200)
    return res

if __name__ == "__main__":
    app.run(debug=True)