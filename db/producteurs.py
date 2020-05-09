# Import des producteurs avec coordonnées

import csv
import pymysql
import re

# Fonction nettoyage
def input_cleaner(text_user):
    text_user = text_user.lower()
    text_user = text_user.strip()
    text_user = re.sub(r'[éèê]','e',text_user)
    text_user = re.sub(r'[ù]','u',text_user)
    text_user = re.sub(r'[àâ]','a',text_user)
    text_user = re.sub(r'[ç]','c',text_user)
    text_user = re.sub(r'[ï]','i',text_user)
    text_user = re.sub(r'arrute-charritte','arraute-charritte',text_user)
    text_user = re.sub(r'les aldudes','aldudes',text_user)
    text_user = re.sub(r'labastide clairence','la-bastide-clairence',text_user)
    text_user = re.sub(r'domintxaine','domezain-berraute',text_user)
    text_user = text_user.replace(' ','-')
    return text_user


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

# Import des lignes en parcourant le csv
with open('scrap/producteurs.csv', mode='r') as csv_file:
    fieldnames = ['nom','maison','mail','tel','code_postal','commune']
    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    next(csv_reader)
    flag = False
    for row in csv_reader:

        commune = input_cleaner(row['commune'])
        sql_loc = "SELECT id FROM localisations l WHERE l.nom_slug LIKE %s"
        cursor.execute(sql_loc, ('%' + commune + '%'))
        result = cursor.fetchone()
        try:
            loc_id = result[0]
        except:
            loc_id = 0
            pass

        sql_rows = "INSERT INTO producteurs(nom, \
        maison, mail, tel, fk_commune_id) \
        VALUES ('%s', '%s', '%s', '%s' , '%i')" % \
        (row['nom'], row['maison'], row['mail'], row['tel'], loc_id)
        
        try:
            cursor.execute(sql_rows)
            db.commit()
        except:
            flag = True
            db.rollback()


# deconnection mysql
db.close()

# Feedback console sur l'import
if (flag):
    print("Erreur à l'import")
else:
    print("Imports effectué sans erreur")