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
from objet.messages import User_msg, Chatbot_msg, Chatbot_list, Chatbot_fiche



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

cat_gen = []
# Fonction utiles
def get_cat_produits():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `nom` FROM `cat_generale`"
            cursor.execute(sql)
            res = cursor.fetchall()
            for cat in res:
                cat_gen.append(cat[0])
            return cat_gen
    except:
        pass

def get_produits(nom):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT categ \
                    FROM cat_produits \
                    WHERE categ LIKE %s"
            cursor.execute(sql,'%' + nom + '%')
            res = cursor.fetchall()
            liste_prod = []
            for prod in res:
                liste_prod.append(prod[0])
            return liste_prod
    except:
        pass


def get_response(text,user):
    user = user
    conversation = []
    conversation.append(User_msg(text))
    text_user = input_cleaner(text)

    # Pour quitter le chatbot
    if (re.search(good_bye, text_user)):
        conversation.append(Chatbot_msg(random.choice(msg_bot)))

    # debug
    elif (text_user == 'fiche'):
        content = {
            'nom': 'Ixuribeherea',
            'commune':'Ayherre',
            'produits':['fromage chèvre bio','chevreau','porc basque','jus de pomme bio']
            }
        conversation.append(Chatbot_fiche(content))

    # Supprime contenu user 
    elif (text_user == "supprimer localisation"):
        print(user)
        user['localisation']= ''
        user['loc_id'] = ''
        user['contexte'] = ''

    # Scenario: cherche produit
    elif ((re.search(r".*produits?.*" ,text_user)) and user['contexte']== ''):
        user['contexte']= 'produit-1'
        conversation.append(Chatbot_msg("Ok voici les catégories de produits:"))
        conversation.append(Chatbot_list(get_cat_produits()))
        conversation.append(Chatbot_msg("Veuillez taper le nom d'un produit que vous cherchez:"))
    
    elif (user['contexte'] == 'produit-1'):
        liste_produits = get_produits(text_user)
        if (len(liste_produits) > 1):
            conversation.append(Chatbot_msg("Voici les produits que j'ai trouvé"))
            conversation.append(Chatbot_list(liste_produits))
        elif (len(liste_produits) == 1):
            conversation.append(Chatbot_msg("J'ai trouvé un produit:"))
            conversation.append(Chatbot_list(liste_produits))
        else:
            conversation.append(Chatbot_msg("Malheureusement je n'ai rien trouvé de correspondant"))
    
    elif (user['contexte'] == 'produit-2'):
        conversation.append(Chatbot_msg("Ok voici les producteurs qui en vende"))

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
                    msg = "Commune reconnue, le code postal est: " + localisations[user['localisation']]
                    conversation.append(Chatbot_msg(msg))

            except:
                print("debug: pas trouvé dans la bdd")
                pass
        else:
            msg = "Aie, commune non reconnue"
            conversation.append(Chatbot_msg(msg))
            user['localisation'] = ''
            conversation.append(Chatbot_msg("""Dites 'au revoir' pour quitter \nSinon dites moi dans quelle commune vous vivez (64 uniquement):"""))
    else:
        if (text_user.lower() == 'ok'):
            with connection.cursor() as cursor:

                sql = "SELECT p.nom FROM producteurs p WHERE p.fk_commune_id = '%s'"
                cursor.execute(sql, (user['loc_id'],))
                result = cursor.fetchall()
                if (result):
                    conversation.append(Chatbot_msg("Ok voici les producteurs:"))
                    liste_prod = []
                    for prod in result:
                        liste_prod.append(prod[0])
                    conversation.append(Chatbot_list(liste_prod))
                else:
                    msg = "Il semble qu'il n'y ait pas de producteur connu dans votre commune"
                    conversation.append(Chatbot_msg(msg))
                    msg = "Voulez-vous que je cherche dans votre canton ?"
                    conversation.append(Chatbot_msg(msg))
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
    print(conversation)
    print(user)
    return conversation