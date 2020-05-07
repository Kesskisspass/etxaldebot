import csv
import re

# test des adresses producteurs

# 1 - import  csv producteur et csv localisation
p = open('./scrap/producteurs.csv','r')
reader = csv.reader(p)
next(reader)
producteurs = {}
for prod in reader:
    producteurs[prod[0]] = prod[5]

l = open('./localisation/communes_64.csv','r')
reader = csv.reader(l)

localisations = {}
for loc in reader:
    localisations[loc[1]] = loc[2]


# 2 - boucle pour rechercher si village reconnu dans le fichier localisation csv
non_reconnus = []
def input_cleaner(text_user):
    text_user = text_user.lower()
    text_user = text_user.strip()
    text_user = re.sub(r'[éèê]','e',text_user)
    text_user = re.sub(r'[ù]','u',text_user)
    text_user = re.sub(r'[àâ]','a',text_user)
    text_user = re.sub(r'[ç]','c',text_user)
    text_user = re.sub(r'[ï]','i',text_user)
    text_user = re.sub(r'st ','saint ',text_user)
    text_user = text_user.replace(' ','-')
    return text_user

for name, commune in producteurs.items():
    if (input_cleaner(commune) in localisations.keys()):
        pass
    else:
        flag = True
        for loc in localisations.keys():
            if(re.search(input_cleaner(commune),loc)):
                print(f"Vous avez tapé: {commune}, vouliez-vous parler de {loc} ?")
                flag = False
        if (flag == True):
            non_reconnus.append(commune)

print(len(non_reconnus),non_reconnus)


# TODO
# arrossa/ahaxe/amendeuix/oneix/tardets/moncayolle/labastide/lichans -> si le text user est compris dans un nom -> on transforme
# domintxaine: nom en basque
    