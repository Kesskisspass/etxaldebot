# Import des communes avec coordonnées GPS en BDD

import csv
import pymysql

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS communes")

sql_table = """CREATE TABLE communes (
   id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
   nom  CHAR(50) NOT NULL,
   nom_slug  CHAR(50) NOT NULL,
   code_postal CHAR(6),
   longitude CHAR(30),  
   latitude CHAR(30) )"""
cursor.execute(sql_table)

# Import des lignes en parcourant le csv
with open('static/cav/communes_64.csv', mode='r') as csv_file:
    fieldnames = ['nom_commune','slug','codepostal','latitude','longitude']
    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    flag = False
    for row in csv_reader:

        sql_rows = "INSERT INTO communes(nom, \
        nom_slug, code_postal, latitude, longitude) \
        VALUES ('%s', '%s', '%s', '%s', '%s' )" % \
        (row['nom_commune'], row['slug'], row['codepostal'], row['latitude'],row['longitude'])
        
        try:
            cursor.execute(sql_rows)
            db.commit()
        except:

            print("Erreur", row['nom_commune'])
            flag = True
            db.rollback()

# deconnection mysql
db.close()

# Feedback console sur l'import
if (flag):
    print("Erreur à l'import")
else:
    print("Imports effectué sans erreur")
