# Import des communes avec coordonnées GPS en BDD

import csv
import pymysql


db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

with open('localisation/communes_64.csv', mode='r') as csv_file:
    fieldnames = ['nom_commune','slug','codepostal','latitude','longitude']
    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    flag = False
    for row in csv_reader:

        sql = "INSERT INTO localisations(NOM, \
        NOM_SLUG, CODE_POSTAL, LONGITUDE, LATITUDE) \
        VALUES ('%s', '%s', '%s', '%s', '%s' )" % \
        (row['nom_commune'], row['slug'], row['codepostal'], row['latitude'],row['longitude'])
        
        # print(row['nom_commune'], row['slug'], row['codepostal'], row['latitude'],row['longitude'])
        
        try:
        # Execute the SQL command
            cursor.execute(sql)
        # Commit your changes in the database
            db.commit()
        except:
        # Rollback in case there is any error
            print("Erreur", row['nom_commune'])
            flag = True
            db.rollback()
if (flag):
    print("Erreur à l'import")
else:
    print("Imports effectué sans erreur")