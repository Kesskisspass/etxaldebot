# Import des catégories produits avec colonne bio (1/0)
import re
import csv
import pymysql

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS cat_generale")

sql_table = """CREATE TABLE cat_generale (
   id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
   nom  CHAR(100) NOT NULL
   )"""
cursor.execute(sql_table)

# Import des lignes en parcourant le csv
with open('scrap/categ_prod.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    flag = False
    for row in csv_reader:
        test = row[0].lower().strip()
        #print(test)
        try:
            if(re.search(r'.*fromages?.*|.*lait.*',test).group()):
                sql_rows = "INSERT INTO cat_generale(nom) \
                VALUES ('fromage et produits laitier' )"
        
                try:
                    cursor.execute(sql_rows)
                    db.commit()
                except:

                    print("Erreur", cat)
                    flag = True
                    db.rollback()
        except:
            pass