from flask import jsonify, make_response
import re
import random
from modules.db import get_cat_produits, get_produits, get_all_producteurs_with_coord, get_info_prod
from modules.distance import find_commune,calc_distance

input_bye = r"(au revoir)|(a bientot)|quit|ciao|(hasta la vista)|(a ?\+)"
bot_bye = ["Au revoir !", "À bientôt", "À très vite","Ciao ciao"]

# Fonction qui renvoie une entrée "nettoyée"
def input_cleaner(text):
    text = text.lower()
    text = text.strip()
    text = re.sub(r'[àâ]','a',text)
    text = re.sub(r'[éèê]','e',text)
    text = re.sub(r'[ï]','i',text)
    text = re.sub(r'[ô]','o',text)
    text = re.sub(r'[ù]','u',text)
    text = re.sub(r'[ç]','c',text)
    return text

def create_par_msg(text):
    dic = {"content":"p","message":text}
    return dic

def create_liste_msg(liste):
    dic = {"content":"l","message":liste}
    return dic

def create_links_produits(liste):
    dic = {"content":"links_produits","message":liste}
    return dic

def create_links_producteurs(liste):
    dic = {"content":"links_producteurs","message":liste}
    return dic

#############
## CHATBOT ##
#############

def get_response(req,user):

    liste_res = []
    req = input_cleaner(req['question'])

    if (re.search(input_bye, req)):
        liste_res.append(create_par_msg(random.choice(bot_bye)))


    elif (req == 'autre recherche'):
        user['contexte'] = ''
        liste_res.append(create_par_msg("Ok que cherchez vous ? des produits ou des producteurs?:"))

    # Scenario: cherche produit
    elif ((re.search(r".*produits?.*" ,req)) and user['contexte']== ''):
        user['contexte']= 'produit-1'
        liste_res.append(create_par_msg("Ok voici les catégories de produits:"))
        liste_res.append(create_liste_msg(get_cat_produits()))
        liste_res.append(create_par_msg("Veuillez taper le nom d'un produit que vous cherchez:"))

    elif (user['contexte'] == 'produit-1'):
        liste_produits = get_produits(req)
        if (len(liste_produits) > 1):
            liste_res.append(create_par_msg("Voici les produits que j'ai trouvé"))
            liste_res.append(create_links_produits(liste_produits))
            liste_res.append(create_par_msg("Cliquez sur un produit pour voir les producteurs qui en propose"))
        elif (len(liste_produits) == 1):
            liste_res.append(create_par_msg("J'ai trouvé un produit:"))
            liste_res.append(create_links_produits(liste_produits))
        else:
            liste_res.append(create_par_msg("Malheureusement je n'ai rien trouvé de correspondant"))

    # Scénario: recherche producteur
    elif ((re.search(r".*producteurs?.*" ,req)) and user['contexte']== ''):
        user['contexte']= 'producteur-1'
        liste_res.append(create_par_msg("Ok, pour trouver les producteurs les plus proche de chez vous, j'ai besoin de connaitre le nom de votre commune (uniquement 64):"))
    
    elif(user['contexte'] == 'producteur-1'):
        response = find_commune(req)
        if(response["found"]==1):
            user['localisation'] = response['localisation']
            user['longitude'] = response['longitude']
            user['latitude'] = response['latitude']
            user['contexte'] = 'producteur-2'
            liste_res.append(create_par_msg(find_commune(req)["msg"]))

            prods = get_all_producteurs_with_coord()
            liste_dist = []
            for prod in prods:
                liste_dist.append(calc_distance(user,prod))
            liste_dist.sort(key=lambda tup: tup[1])
            liste_prod = []
            for prod in liste_dist[:5]:
                liste_prod.append(get_info_prod(prod[0]))
            liste_res.append(create_links_producteurs(liste_prod))

        else:
            liste_res.append(create_par_msg(find_commune(req)["msg"]))

    else:
        liste_res.append(create_par_msg("Désolé mais je n'ai pas compris"))
    
    # debug
    print(liste_res)
    
    res = make_response(jsonify(liste_res), 200)
    return res
