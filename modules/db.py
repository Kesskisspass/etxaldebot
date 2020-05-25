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
            sql = "SELECT categ \
                    FROM cat_produits \
                    WHERE categ LIKE %s"
            cursor.execute(sql,'%' + nom + '%')
            res = cursor.fetchall()
            liste_prod = []
            for prod in res:
                liste_prod.append(prod[0])
            return liste_prod
    except:
        pass

def get_produits_from_cat(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `categ`,`id`\
                    FROM `cat_produits` \
                    WHERE `fk_cat_gen_id` = %s"
            cursor.execute(sql,int(id))
            res = cursor.fetchall()
            liste_prod = []
            for prod in res:
                print(prod)
                liste_prod.append(prod)
            return liste_prod
    except:
        pass
