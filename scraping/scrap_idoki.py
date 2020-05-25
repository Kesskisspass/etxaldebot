import requests
from bs4 import BeautifulSoup
import re
import csv

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

categories_produits = dict()

# Création d'un csv qui regroupe toutes les infos producteur

with open('static/csv/producteurs.csv', 'w', newline='') as f:
    fieldnames = ['nom','maison','mail','tel','code_postal','commune','categ_prod','produits','lieux','horaires']
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

        # Nom
        dico['nom'] = infos.find("h1").text

        # Maison
        dico['maison'] = infos.find("h3").text

        # Mail
        mail = infos.find("a")
        mail = str(mail)
        mail = re.sub(r'<a href=".*">','',mail)
        mail = mail.replace('<img alt="(at)" src="fileadmin/templates/site/img/at.gif"/>','@')
        mail = re.sub(r'( </a>)|(</a>)','',mail)
        if ("@" in mail):
            dico['mail'] = mail

        # Tel
        tel = re.search(r"(([0-9]+ [0-9]+ [0-9]+ [0-9]+ [0-9]+))",str(infos))
        if tel:
            tel = re.sub(" ","",tel.group())
            dico['tel'] = tel

        # Code postal
        code_postal = re.search(r"([0-9][0-9] [0-9][0-9][0-9])|([0-9][0-9][0-9][0-9][0-9])",str(infos))
        if code_postal:
            code_postal = re.sub(" ","",code_postal.group())
            dico['code_postal'] = code_postal

        # Village
        commune = re.search(r"(([A-ZÏÈÉ\-]+)([A-ZÏÈÉ \-]+)? ?/)|([A-Z]+\-[A-Z]+)", str(infos))
        if commune:
            commune = re.sub(r"( /)|(/)","",commune.group())
            dico['commune'] = commune

        # Produits
        for div in soup.find_all("div", attrs={"class":"whitecard row"}):
            if ('Mes produits' in div.text):
                
                # Détail des produits
                try:
                    prod = div.find_all("li")
                    produits = []
                    for produit in prod:
                        produit = produit.text
                        produit = re.sub(r"\r","", produit)
                        produit = re.sub(r"\n"," ", produit)
                        produit = re.sub(r"  "," ", produit)
                        produits.append(produit)
                    dico['produits'] = produits
                except:
                    pass
                
                # Catégorie des produits
                try:
                    categ_prod = []
                    cat = div.find_all("img")
                    for categ in cat:
                        categorie = categ['title']
                        categ_prod.append(categorie)

                        if (categorie in categories_produits):
                            categories_produits[categorie] += 1
                        else:
                            categories_produits[categorie] = 1   

                    dico['categ_prod'] = categ_prod
                except:
                    pass

        # Lieux de vente
        for div in soup.find_all("div", attrs={"class":"whitecard row"}):
            if ('lieux' in div.text):
                try:
                    lieu = div.find_all("li")
                    lieux = []
                    for li in lieu:
                        li = li.text
                        lieux.append(li)
                    dico['lieux'] = lieux
                except:
                    pass

        # Vente à la ferme (horaires)
        for div in soup.find_all("div", attrs={"class":"whitecard row"}):
            if ('Vente à la ferme' in div.text):
                try:
                    horaires = div.find("div", attrs={"class":"col-sm-9"}).text
                    dico['horaires'] = horaires
                except:
                    pass

        # Ajout au fichier csv
        writer.writerow(dico)

# Création csv des catégories de produits (et nombre de producteurs qui le propose)
f = open('static/csv/categ_prod.csv', 'w', newline='')
with f:
    writer = csv.writer(f)
    writer.writerow(['categorie','bio','nombre'])
    for cat, nb in categories_produits.items():

        if (re.search(r'.* bios?',cat)):
            writer.writerow([cat, 1, nb])
        else:
            writer.writerow([cat, 0, nb])
