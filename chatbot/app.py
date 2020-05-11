# coding: utf8
import csv
import re
import random
import string
from textblob import TextBlob
from textblob_fr import PatternAnalyzer
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='etxaldebot')

# Chargements des données dans les csv
l = open('./localisation/communes_64.csv','r')
reader = csv.reader(l)
localisations = {}

# Permet de ne pas intégrer la ligne de header
#next(reader)

for loc in reader:
    localisations[loc[1]] = loc[2]



# Fonction nettoyage input user
def input_cleaner(text_user):
    text_user = text_user.lower()
    text_user = re.sub(r'[éèê]','e',text_user)
    text_user = re.sub(r'[ù]','u',text_user)
    text_user = re.sub(r'[àâ]','a',text_user)
    text_user = re.sub(r'[ç]','c',text_user)
    text_user = re.sub(r'[ï]','i',text_user)
    return text_user

# Inputs et réponses
good_bye = r"au revoir|quit|ciao|hasta la vista|à \+"
msg_bot = ["Au revoir!", "à bientôt", "à très vite!","ciao ciao"]

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

flag = True
flag_search_cp = False
print("""Bienvenue, \nDites 'au revoir' pour quitter \nD'abord dites moi dans quelle commune vous vivez (64 uniquement):""")
while (flag == True):
    text_user = input("> ")

    # Processing entrée utilisateur
    text_user = input_cleaner(text_user)

    # Pour quitter le chatbot
    if (re.search(good_bye, text_user)):
        print(random.choice(msg_bot))
        print(user)
        flag = False


    # Test localisation
    elif(user['localisation']==''):
        text_user = re.sub(r'st ','saint ',text_user)
        text_user = text_user.replace(' ','-')
        if (text_user in localisations.keys()):
            user['localisation'] = text_user
            try:
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `id` FROM `communes` WHERE `nom_slug`=%s"
                    cursor.execute(sql, (user['localisation'],))
                    user['loc_id'] = cursor.fetchone()[0]
                    print("commune reconnue, le code postal est: ", localisations[user['localisation']])
                    print(user)
                    print("Je peux vous aider à trouver des producteurs près de chez vous ? OK?")
            except:
                pass
        else:
            print("Houston, commune non reconnue")
            user['localisation'] = ''
            print("""Dites 'au revoir' pour quitter \nSinon dites moi dans quelle commune vous vivez (64 uniquement):""")
            print(user)
    else:
        if (text_user.lower() == 'ok'):
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT p.nom FROM producteurs p WHERE p.fk_commune_id = '%s'"
                cursor.execute(sql, (user['loc_id'],))
                result = cursor.fetchall()
                if (result):
                    print("Ok voici les producteurs:")
                    for prod in result:
                        print (prod[0])
                else:
                    print("Il semble qu'il n'y ait pas de producteur connu dans votre commune")
                    print("Voulez-vous que je cherche dans votre canton ?")
                    text_user = input("> ")
                    if (text_user == 'ok'):
                        flag_search_cp = True
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
            print(user)
