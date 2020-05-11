# coding: utf8
import csv
import re
import random
import string
from textblob import TextBlob
from textblob_fr import PatternAnalyzer

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
    else:
        text_user = re.sub(r'st ','saint ',text_user)
        text_user = text_user.replace(' ','-')
        if (text_user in localisations.keys()):
            user['localisation'] = text_user
            print("commune reconnue, le code postal est: ", localisations[user['localisation']])
            print(user)
        else:
            print("Houston, commune non reconnue")
            user['localisation'] = ''
            print(user)