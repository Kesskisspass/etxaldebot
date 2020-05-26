import pymysql.cursors

connection = pymysql.connect(host='localhost',
                            user='root',
                            password='root',
                            db='etxaldebot')


def get_cat_produits():
    cat_gen = []
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `nom` FROM `cat_generale`"
            cursor.execute(sql)
            res = cursor.fetchall()
            for cat in res:
                cat_gen.append(cat[0])
            return cat_gen
    except:
        pass


def get_produits(nom):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT categ , id\
                    FROM cat_produits \
                    WHERE categ LIKE %s"
            cursor.execute(sql,'%' + nom + '%')
            res = cursor.fetchall()
            liste_prod = []
            for prod in res:
                liste_prod.append(prod)
            return liste_prod
    except:
        pass
# A modifier avec la nouvelle table xixtroak
def get_produits_from_cat(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `article` \
                    FROM `reco_produits` \
                    WHERE `cat_id` = %s"
            cursor.execute(sql,int(id))
            res = cursor.fetchall()
            liste_prod = []
            for prod in res:
                liste_prod.append(prod)
            return liste_prod
    except:
        pass

def get_producteurs_from_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT p.nom, c.nom, p.id \
                    FROM `producteurs` p \
                    JOIN `producteurs_categories` pc \
                    ON pc.`fk_producteur_id` = p.id \
                    JOIN `cat_produits` cp \
                    ON pc.`fk_cat_produit_id` = cp.id \
                    JOIN `communes`c \
                    ON c.id = p.fk_commune_id \
                    WHERE cp.id = %s "
            cursor.execute(sql,int(id))
            res = cursor.fetchall()
            liste_prod = []
            for prod in res:
                print(prod)
                liste_prod.append(prod)
            return liste_prod
    except:
        pass

def get_producteur_from_id(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT p.nom, c.nom, p.mail, p.tel \
                    FROM `producteurs` p \
                    JOIN `communes`c \
                    ON c.id = p.fk_commune_id \
                    WHERE p.id = %s "
            cursor.execute(sql,int(id))
            res = cursor.fetchone()
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT cp.categ \
                            FROM cat_produits cp \
                            JOIN `producteurs_categories` pc \
                            ON pc.`fk_cat_produit_id` = cp.id \
                            JOIN `producteurs` p \
                            ON p.`id` = pc.`fk_producteur_id` \
                            WHERE p.id = %s "
                    cursor.execute(sql,int(id))
                    res2 = cursor.fetchall()
                    liste_produits = []
                    for prod in res2:
                        liste_produits.append(prod[0])
                    return (res, liste_produits)
            except:
                pass
    except:
        pass
