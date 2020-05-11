# Création de la table cat_generale

import pymysql

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS cat_generale")

sql_table = """CREATE TABLE cat_generale (
   id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nom CHAR(100) NOT NULL
   )"""
cursor.execute(sql_table)

liste = ['fromages et produits laitiers','fruits et légumes','viandes','boissons','autres']

sql_rows = "INSERT INTO cat_generale(nom)  VALUES ('%s')"          
try:
    cursor.executemany(sql_rows,liste)
    db.commit()
except:
    print("Erreur", liste)
    db.rollback()
db.close()