# Création de la table intermediaire producteurs/categ_produits

import csv
import pymysql
import ast

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS producteurs_categories")

sql_table = """CREATE TABLE producteurs_categories (
   fk_producteur_id  INT NOT NULL,
   fk_cat_produit_id INT NOT NULL,

   FOREIGN KEY (fk_producteur_id) REFERENCES producteurs(id),
   FOREIGN KEY (fk_cat_produit_id) REFERENCES cat_produits(id) )"""
cursor.execute(sql_table)

# Import des lignes en parcourant le csv
with open('scrap/producteurs.csv', mode='r') as csv_file:
    fieldnames = ['nom','maison','mail','tel','code_postal','commune','categ_prod']
    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    next(csv_reader)
    flag = False
    for row in csv_reader:
       sql_prod = "SELECT id FROM producteurs p WHERE p.nom = %s"
       cursor.execute(sql_prod, (row['nom']))
       result = cursor.fetchone()
       prod_id = result[0]

       # ast -> Transformation string de bdd en liste python
       for cat in ast.literal_eval(row['categ_prod']):
         cat = cat.lower()
         cat = cat.replace('\'',' ')
         sql_cat = "SELECT id FROM cat_produits c WHERE c.categ = %s"
         cursor.execute(sql_cat, cat)
         result = cursor.fetchone()
         try:
            cat_id = result[0]
            sql_rows = "INSERT INTO producteurs_categories(fk_producteur_id,fk_cat_produit_id) \
            VALUES ('%i', '%i' )" % \
            (int(prod_id), int(cat_id ))
        
            try:
               cursor.execute(sql_rows)
               db.commit()
            except:
               flag = True
               db.rollback()
         except:
            print('erreur',cat)
            pass

# deconnection mysql
db.close()
