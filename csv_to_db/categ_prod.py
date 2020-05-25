# Import des catégories produits avec colonne bio (1/0)

import csv
import pymysql
import re

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS cat_produits")

sql_table = """CREATE TABLE cat_produits (
   id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
   categ  CHAR(100) NOT NULL,
   bio  INT NOT NULL,
   fk_cat_gen_id INT,

   FOREIGN KEY (fk_cat_gen_id) REFERENCES cat_generale(id)
   )"""
cursor.execute(sql_table)

# Import des lignes en parcourant le csv
with open('static/csv/categ_prod.csv', mode='r') as csv_file:
    fieldnames = ['categ','bio']
    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    flag = False
    for row in csv_reader:
        cat = row['categ'].strip()
        cat = cat.lower()
        cat = cat.replace('\'',' ')
        cat_gen = 5
        try:
            fromage = re.match(r'.*fromages?.*|.*lait.*',cat)
            viande = re.match(r'.*viandes?.*|.*poulets?.*|.*pigeonneaux?.*|.*porcs?.*|.*canards?.*',cat)
            fruit = re.match(r'.*fruits?.*|.*legumes?.*|.*légumes?.*',cat)
            boisson = re.match(r'.*cidres?.*|.*jus?.*|.*vins?.*',cat)
            if(fromage):
                cat_gen = 1
            elif(fruit):
                cat_gen = 2
            elif(viande):
                cat_gen = 3
            elif(boisson):
                cat_gen = 4
        except:
            cat_gen = 5
        sql_rows = "INSERT INTO cat_produits(categ,bio,fk_cat_gen_id) \
        VALUES ('%s', '%i', '%i' )" % \
        (cat, int(row['bio']),cat_gen)
        
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