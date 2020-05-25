from math import acos, cos, sin, radians
import csv

def find_commune(name):
    with open('localisation/communes_64.csv', mode='r') as csv_file:
        fieldnames = ['nom_commune','slug','codepostal','latitude','longitude']
        csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
        flag = False
        name = name.lower()
        name = name.replace(" ","-")
        name = name.replace("'","")
        name = name.replace("st","saint")
        for row in csv_reader:
            if (row['slug'] == name):
                flag = True
                return(float(row['latitude']),float(row['longitude']))
        if (flag == False):
            print("Commune non trouvée")

# Test calcul distance avec deux communes
c1 = input("Veuillez entrer le nom de la première commune:\n")
p1 = find_commune(c1)
c2 = input("Veuillez entrer le nom de la seconde commune:\n")
p2 = find_commune(c2)

# Calcul distance
distance = acos(sin(radians(p1[0]))*sin(radians(p2[0]))+cos(radians(p1[0]))*cos(radians(p2[0]))*cos(radians(p1[1]-p2[1])))*6371
print(f"La distance entre les deux communes est de : {round(distance,2)}km")