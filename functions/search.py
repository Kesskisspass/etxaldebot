import csv
import re
from math import acos, cos, sin, radians

# Fonction qui renvoie une entrée "nettoyée"
def input_cleaner(text):
    text = text.lower()
    text = text.strip()
    text = re.sub(r'[éèê]','e',text)
    text = re.sub(r'[ù]','u',text)
    text = re.sub(r'[àâ]','a',text)
    text = re.sub(r'[ç]','c',text)
    text = re.sub(r'[ï]','i',text)
    text = re.sub(r'st ','saint ',text)
    text = text.replace(' ','-')
    return text

# Fonction qui renvoie une commune ou None si non-trouvée
def find_commune(text):
    # On nettoie l'entrée
    text = input_cleaner(text)

    # On traite les cas particuliers
    text = re.sub(r'arrute-charritte','arraute-charritte',text)
    text = re.sub(r'les aldudes','aldudes',text)
    text = re.sub(r'labastide clairence','la-bastide-clairence',text)
    text = re.sub(r'domintxaine','domezain-berraute',text)

    # On récupère la liste des communes
    l = open('./localisation/communes_64.csv','r')
    reader = csv.reader(l)
    localisations = {}
    for loc in reader:
        localisations[loc[1]] = loc[2]

    # On cherche l'entrée dans le dico de localisations    
    if (text in localisations.keys()):
        pass
    else:
        for loc in localisations.keys():
            if(re.search(text,loc)):
                text = loc
            else:
                text = None
    return text

def return_coord(commune):
    commune = find_commune(commune)
    with open('localisation/communes_64.csv', mode='r') as csv_file:
        fieldnames = ['nom_commune','slug','codepostal','latitude','longitude']
        csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
        flag = False
        for row in csv_reader:
            if (row['slug'] == commune):
                flag = True
                return(float(row['latitude']),float(row['longitude']))
        if (flag == False):
            return None

# Fonction qui renvoie la distance entre deux communes (km)
def find_distance(commune_1,commune_2):
    
        p1 = return_coord(commune_1)
        p2 = return_coord(commune_2)

        # Calcul distance
        distance = acos(sin(radians(p1[0]))*sin(radians(p2[0]))+cos(radians(p1[0]))*cos(radians(p2[0]))*cos(radians(p1[1]-p2[1])))*6371
        return distance


    