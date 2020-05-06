# coding: utf8
import re
import random
import string
from textblob import TextBlob
from textblob_fr import PatternAnalyzer

# Fonction nettoyage input user
def input_cleaner(text_user):
    text_user = text_user.lower()
    text_user = re.sub(r'[éèê]','e',text_user)
    text_user = re.sub(r'[ù]','u',text_user)
    text_user = re.sub(r'[àâ]','a',text_user)
    text_user = re.sub(r'[ç]','c',text_user)
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
print("""Bienvenue, je suis là pour vous aider à trouver des producteurs fermier autour de chez vous \nÉcrivez votre question : \nDites moi au revoir pour quitter \nD'abord dites moi dans quelle commune vous vivez pour que je puisse vous proposer des producteurs près de chez vous:""")
while (flag == True):
    text_user = input("> ")

    # Processing entrée utilisateur
    text_user = input_cleaner(text_user)

    # Pour quitter le chatbot
    if (re.search(good_bye, text_user)):
        print(random.choice(msg_bot))
        flag = False


    # Test localisation
    else:
        text_user = text_user.replace('st','saint')
        text_user = text_user.replace(' ','-')
        print(text_user)