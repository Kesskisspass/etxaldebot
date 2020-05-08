# Import des communes avec coordonnées GPS en BDD

import csv
import pymysql

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS localisations")

sql_table = """CREATE TABLE localisations (
   ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
   NOM  CHAR(50) NOT NULL,
   NOM_SLUG  CHAR(50) NOT NULL,
   CODE_POSTAL  CHAR(6),
   LONGITUDE CHAR(30),  
   LATITUDE CHAR(30) )"""
cursor.execute(sql_table)

# Import des lignes en parcourant le csv
with open('localisation/communes_64.csv', mode='r') as csv_file:
    fieldnames = ['nom_commune','slug','codepostal','latitude','longitude']
    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    flag = False
    for row in csv_reader:

        sql_rows = "INSERT INTO localisations(NOM, \
        NOM_SLUG, CODE_POSTAL, LONGITUDE, LATITUDE) \
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
