# coding: utf8
import csv
import re
import random
import string
from textblob import TextBlob
from textblob_fr import PatternAnalyzer
import pymysql
from functions.search import input_cleaner, find_commune
from flask import Flask, render_template

# TODO : Créer des classes pour les types de messages (paragraphe, liste, liens)

connection = pymysql.connect(host='localhost',
                            user='root',
                            password='root',
                            db='etxaldebot')

# Chargements des données dans les csv
l = open('./localisation/communes_64.csv','r')
reader = csv.reader(l)
localisations = {}

for loc in reader:
    localisations[loc[1]] = loc[2]


# Inputs et réponses
good_bye = r"(au revoir)|quit|ciao|(hasta la vista)|(a \+)"
msg_bot = ["Au revoir !", "À bientôt", "À très vite","Ciao ciao"]

inp_salut = r"bonjour.*?|salut.*?|.ep.*?|yo.*?|coucou.*?"
msg_salutation = [
"Bonjour",
"Salut",
"Quel plaisir de pouvoir discuter un peu avec vous",
"iep",
"Egun On"
]

# On stocke les infos utilisateur dans un dico
user = {'localisation':''}

def get_response(text):
    response = []
    text_user = input_cleaner(text)

    # Pour quitter le chatbot
    if (re.search(good_bye, text_user)):
        msg = {'type':'p','content':random.choice(msg_bot)}
        response.append(msg)

    # Test localisation
    elif(user['localisation'] == ''):
        text_user = find_commune(text_user)
        if (text_user in localisations.keys()):
            user['localisation'] = text_user
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT `id` FROM `communes` WHERE `nom_slug`=%s"
                    cursor.execute(sql, (user['localisation'],))
                    user['loc_id'] = cursor.fetchone()[0]
                    msg = {"type": 'p', 'content': "Commune reconnue, le code postal est: " + localisations[user['localisation']]}
                    response.append(msg)
                    msg = {'type':'p', 'content': "Je peux vous aider à trouver des producteurs près de chez vous ? OK?"}
                    response.append(msg)
            except:
                print("debug: pas trouvé dans la bdd")
                pass
        else:
            print("Houston, commune non reconnue")
            user['localisation'] = ''
            print("""Dites 'au revoir' pour quitter \nSinon dites moi dans quelle commune vous vivez (64 uniquement):""")
            print(user)
    else:
        if (text_user.lower() == 'ok'):
            with connection.cursor() as cursor:

                sql = "SELECT p.nom FROM producteurs p WHERE p.fk_commune_id = '%s'"
                cursor.execute(sql, (user['loc_id'],))
                result = cursor.fetchall()
                if (result):
                    msg = {'type':'p', 'content': "Ok voici les producteurs:"}
                    response.append(msg)
                    liste_prod = []
                    for prod in result:
                        liste_prod.append(prod[0])
                    msg = {'type':'l','content':liste_prod}
                    response.append(msg)
                else:
                    print("Il semble qu'il n'y ait pas de producteur connu dans votre commune")
                    print("Voulez-vous que je cherche dans votre canton ?")
                    text_user = input("> ")
                    if (text_user == 'ok'):

                        with connection.cursor() as cursor:
                            sql = "SELECT p.nom, c.nom \
                                    FROM producteurs p \
                                    JOIN communes c \
                                    ON p.fk_commune_id = c.id \
                                    WHERE c.code_postal = ( \
                                    SELECT c.code_postal \
                                    FROM communes c\
                                    WHERE c.id = '%s')"
                            cursor.execute(sql, (user['loc_id'],))
                            result = cursor.fetchall()
                            if (result):
                                print("Ok voici les producteurs:")
                                for prod in result:
                                    print (prod[0],"à",prod[1])
                            else:
                                print("pas de résultat dans le code-postal") # Chercher avec localisations les moins éloignées
    return response