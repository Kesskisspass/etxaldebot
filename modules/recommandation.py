import pickle
import csv
import sklearn

def panier_to_vector(liste):

    vector = []
    dico = {"agrumes" : 0 ,"ail" : 0 ,"assortiment" : 0 ,"aubergine" : 0 ,"autre" : 0 ,"betterave" : 0,
       "beurre" : 0 ,"blette" : 0 ,"breuil" : 0 ,"carotte" : 0 ,"celeri" : 0 ,"cerises" : 0 ,"chou" : 0,
       "ciboulette" : 0 ,"compote" : 0 ,"concombre" : 0 ,"confiture" : 0 ,"coulis" : 0 ,"courge" : 0,
       "creme fraiche" : 0 ,"echalote" : 0 ,"epinard" : 0 ,"farine" : 0 ,"fenouil" : 0 ,"feves" : 0,
       "fromage blanc" : 0 ,"fromage de brebis fermier" : 0 ,"fromage de chèvre" : 0,
       "fromage de vache affiné" : 0 ,"fromage pérail de brebis" : 0 ,"haricots verts" :0,
       "huile" : 0 ,"jus ou sirop" : 0 ,"kiwi" : 0 ,"lait" : 0 ,"mamia" : 0 ,"melon" : 0 ,"miel" : 0,
       "navet" : 0 ,"oeufs" : 0 ,"oignon" : 0 ,"pain d'épices" : 0 ,"pastèque" : 0 ,"patidou" : 0,
       "persil" : 0 ,"petit pois" : 0 ,"piment" : 0 ,"pintade" : 0 ,"poireaux" : 0 ,"poivron" : 0,
       "polenta" : 0 ,"pollen" : 0 ,"pomme de terre" : 0 ,"pommes" : 0 ,"potimarron" : 0 ,"poule" : 0,
       "poulet" : 0 ,"pâte à tartiner" : 0 ,"pâtes" : 0 ,"pêches" : 0 ,"radis" : 0 ,"salade" : 0,
       "savon" : 0 ,"soupe" : 0 ,"tisane" : 0 ,"tomate" : 0 ,"tomme de vache fraîche" : 0,
       "viande de chèvre ou chevreau" : 0 ,"viande de porc" : 0 ,"viande de veau" : 0,
       "vin ou cidre" : 0 ,"yaourt" : 0}

    for article in liste:
        dico[article] += 1

    for value in dico.values():
        vector.append(value)
    
    return vector

def get_reco(liste_panier):
    # On transforme la liste de produit en vecteur pour notre modèle
    vector = panier_to_vector(liste_panier)

    # Chargement du modèle
    filename = "recommandation/kmeans_model.sav"
    loaded_model = pickle.load(open(filename, "rb"))

    # Chargement des données (produits les plus fréquents par classe)
    csv_path = "recommandation/df_export.csv"
    with open(csv_path, newline="") as csvfile:
        classe_top_article = []
        top_classe = csv.reader(csvfile, delimiter=",")
        next(top_classe)
        for classe in top_classe:
            classe_top_article.append(classe)

    # On fait notre prediction de classe
    print("La classe du panier est:",loaded_model.predict([vector])[0])

    # Maintenant qu'on a obtenu la classe du panier, on va chercher les articles à proposer
    produits_classe = classe_top_article[loaded_model.predict([vector])[0]]

    # On va supprimer de cette liste les articles du panier utilisateur pour lui en proposer seulement de nouveaux
    response = []
    for product in produits_classe:
        if product not in liste_panier:
            response.append(product)
    
    # Et on retourne la réponse
    return response

# Debug
# liste = ["aubergine","fromage de chèvre","tomate","jus ou sirop"]
# get_reco(liste)