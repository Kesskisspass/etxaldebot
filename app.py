from flask import Flask, render_template, request, redirect
from modules.chatbot import get_response
from modules.db import get_produits_from_cat
from flask import jsonify, make_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/send_message', methods=['POST'])
def create_entry():
    req = request.get_json()

    return get_response(req)

@app.route('/recommandation')
def recommandation():
    return render_template("recommandation.html")

@app.route('/get_product', methods=['POST'])
def fill_product():
    cat_id = request.get_json()
    liste = get_produits_from_cat(cat_id['categorie'])
    res = make_response(jsonify(liste), 200)
    return res

if __name__ == "__main__":
    app.run(debug=True)