import requests
from bs4 import BeautifulSoup
import re

# Récupération de toutes les urls des pages producteurs
urls_prod = []
base = "https://www.producteurs-fermiers-pays-basque.fr/fr/nos-producteurs-fermiers/?tx_idoki_pi1%5Bcat%5D=0&tx_idoki_pi1%5Bville%5D=0&tx_idoki_pi1%5Bsubmit%5D=notrand&tx_idoki_pi1%5Bpage%5D="
for i in range(14):
    url = base + str(i)
    urls_prod.append(url)

# Récupération fiche producteur par page
links = []

for url in urls_prod:
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src,'lxml')

    # la div qui contient les fiches des 6 producteurs de la page
    prods = soup.find("div", attrs={u"class":"row list"})

    # On récupère le lien de leur page producteur Idoki
    for link in prods.find_all('a'):
        links.append(link.get('href'))

# Penser à rajouter la base url: https://www.producteurs-fermiers-pays-basque.fr/

# Création d'un csv qui regroupe toutes les infos producteur
import csv

with open('producteurs.csv', 'w', newline='') as f:
    fieldnames = ['nom','maison']
    writer = csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()
    
    for link in links:
        link = 'https://www.producteurs-fermiers-pays-basque.fr/' + link
        result = requests.get(link)
        src = result.content
        soup = BeautifulSoup(src,'lxml')
        infos = soup.find("div", attrs={u"class":"description"})

        # Récupérer les infos producteur dans un dico
        dico = {}
        dico['nom'] = infos.find("h1").text
        dico['maison'] = infos.find("h3").text

        # Ajout au fichier csv
        writer.writerow(dico)
