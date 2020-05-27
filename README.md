# EtxaldeBot

## Résumé: 
Créer un chatbot qui s'adresse à des utilisateurs du Pays-Basque et qui souhaitent pouvoir rapidement chercher et trouver des produits fermiers aux alentours de chez eux.   
Le chatbot doit pouvoir leur indiquer où trouver les produits recherchés selon différents critères (localisation, produit bio ou pas, type de produit..)
Enfin, après analyse des produits recherchés par l'utilisateur, le chatbot doit pouvoir effectuer des recommandations pour d'autres produits.

## Outils:
- Récupération des informations: scraping pour extraire les données de différents sites (BeautifulSoup)
- Stockage des données en BDD relationelle (MariaDB ou PostGreSQL)
- Création du chatbot: Python
- Pour effectuer les recommandations aux utilisateurs: utilisation d'un modèle de machine learning (Kmeans)

## Schéma Fonctionnement Général:
![schema](static/img/schema_chatbot.png)

## Schéma Base de données
![bdd](static/img/bdd_etxaldebot.png)