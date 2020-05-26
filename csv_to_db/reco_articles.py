import csv
import pymysql

db = pymysql.connect("localhost","root","root","etxaldebot" )
cursor = db.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS reco_produits")

sql_table = """CREATE TABLE reco_produits (
   article  CHAR(100) NOT NULL UNIQUE,
   cat_id INT NOT NULL
   )"""
cursor.execute(sql_table)

with open('static/csv/reco_articles.csv', mode='r', newline='') as csv_file:
    fieldnames = ['article','cat_id']
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    flag = False
    for row in csv_reader:
        sql_rows = "INSERT INTO reco_produits(article,cat_id) \
        VALUES ('%s', '%i' )" % \
        (row[0], int(row[1]))
        
        try:
            cursor.execute(sql_rows)
            db.commit()
        except:

            print("Erreur", row)
            flag = True
            db.rollback()

# deconnection mysql
db.close()

# Feedback console sur l'import
if (flag):
    print("Erreur à l'import")
else:
    print("Imports effectué sans erreur")