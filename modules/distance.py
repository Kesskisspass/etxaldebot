from math import acos, cos, sin, radians
import csv

def find_commune(name):
    with open('static/csv/communes_64.csv', mode='r') as csv_file:
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
                res = {"found":1,
                "localisation":name,
                "msg":f"Ok voici les producteurs les plus proche de {name.capitalize()}",
                "latitude":float(row['latitude']),
                "longitude":float(row["longitude"])}
                return(res)
        if (flag == False):
            res = {"found":0,"msg":f"Aïe, je ne trouve pas {name.capitalize()}"}
            return(res)


def calc_distance(user,prod):
    print('Longitude',user['longitude'],"Latitude",user['latitude'])
    # print("user latitude:", type(user['latitude']), "user longitude:",type(user['longitude']),"prod latitude:",type(float(prod[3])),"prod longitude:", type(float(prod[4])))
    distance = acos(sin(radians(user['longitude']))*sin(radians(float(prod[4])))+cos(radians(user['longitude']))*cos(radians(float(prod[4])))*cos(radians(user['latitude']-float(prod[3]))))*6371
    return(prod[0],distance)

# Test calcul distance avec deux communes
# c1 = input("Veuillez entrer le nom de la première commune:\n")
# p1 = find_commune(c1)
# c2 = input("Veuillez entrer le nom de la seconde commune:\n")
# p2 = find_commune(c2)

# Calcul distance
# distance = acos(sin(radians(p1[0]))*sin(radians(p2[0]))+cos(radians(p1[0]))*cos(radians(p2[0]))*cos(radians(p1[1]-p2[1])))*6371
# print(f"La distance entre les deux communes est de : {round(distance,2)}km")