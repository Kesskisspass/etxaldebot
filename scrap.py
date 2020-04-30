import requests
from bs4 import BeautifulSoup
import re


# Récupération des info producteurs Lekukoa

# Récupération des pages des points de ventes

result = requests.get('https://www.lekukoa.com/ou-acheter')
src = result.content
soup = BeautifulSoup(src,'lxml')

links = soup.find_all("a", attrs={u"target":"_self"})

urls = []
for link in links:
    try:
        adress = link.attrs['href']
        res = re.match(r'^https://www.lekukoa.com/.*',adress)
        web = res.group(0)
        if web not in urls:
            urls.append(web)
    except:
        pass

# Les 5 premières sont celles du menu de navigation
urls = urls[5:]
#print(len(urls))

# test page Bayonne
result = requests.get('https://www.lekukoa.com/bayonne')
src = result.content
soup = BeautifulSoup(src,'lxml')
fiches = soup.find_all("div", {"class":"mc1inlineContent"})
producteurs = []
for fiche in fiches:
    producteurs.append(fiche)

for prod in producteurs:
    name = prod.find("span", {"style":"font-family:poppins-semibold,poppins,sans-serif;"})
    paras = prod.find_all("p")
    try:
        i = 0
        for para in paras:
            para = para.text
            if para != "":
                print(i, para)
                i += 1
        print("---")
    except:
        pass
    
