# Import des catégories produits avec colonne bio (1/0)

import csv
import pymysql

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS cat_produits")

sql_table = """CREATE TABLE cat_produits (
   id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
   categ  CHAR(100) NOT NULL,
   bio  INT NOT NULL
   )"""
cursor.execute(sql_table)

# Import des lignes en parcourant le csv
with open('scrap/categ_prod.csv', mode='r') as csv_file:
    fieldnames = ['categ','bio']
    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    flag = False
    for row in csv_reader:
        cat = row['categ'].strip()
        cat = cat.lower()
        cat = cat.replace('\'',' ')
        sql_rows = "INSERT INTO cat_produits(categ,bio) \
        VALUES ('%s', '%i' )" % \
        (cat, int(row['bio']))
        
        try:
            cursor.execute(sql_rows)
            db.commit()
        except:

            print("Erreur", cat)
            flag = True
            db.rollback()

# deconnection mysql
db.close()

# Feedback console sur l'import
if (flag):
    print("Erreur à l'import")
else:
    print("Imports effectué sans erreur")