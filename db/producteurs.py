# Import des producteurs avec coordonnées

import csv
import pymysql

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS producteurs")

sql_table = """CREATE TABLE producteurs (
   id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
   nom  CHAR(100) NOT NULL,
   maison  CHAR(100),
   mail CHAR(30),
   tel CHAR(20),
   fk_commune_id INT,

   FOREIGN KEY (fk_commune_id) REFERENCES localisations(id) )"""
cursor.execute(sql_table)


### TODO
# Chercher la localisation dans db
# renvoyer id, 
# puis import dans bdd producteur (fk_localisation_id)


# Import des lignes en parcourant le csv
with open('scrap/producteurs.csv', mode='r') as csv_file:
    fieldnames = ['nom','maison','mail','tel','commune']
    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    flag = False
    for row in csv_reader:

        sql_rows = "INSERT INTO producteurs(nom, \
        maison, mail, tel) \
        VALUES ('%s', '%s', '%s', '%s' )" % \
        (row['nom'], row['maison'], row['mail'], row['tel'])
        
        try:
            cursor.execute(sql_rows)
            db.commit()
        except:

            print("Erreur", row['nom'])
            flag = True
            db.rollback()


# deconnection mysql
db.close()

# Feedback console sur l'import
if (flag):
    print("Erreur à l'import")
else:
    print("Imports effectué sans erreur")