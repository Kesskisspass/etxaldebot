import pymysql

# Open database connection
db = pymysql.connect("localhost","root","root","etxaldebot" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS localisations")

# Create table as per requirement
sql = """CREATE TABLE localisations (
   NOM  CHAR(50) NOT NULL,
   NOM_SLUG  CHAR(50) NOT NULL,
   CODE_POSTAL  CHAR(6),
   LONGITUDE CHAR(30),  
   LATITUDE CHAR(30) )"""
cursor.execute(sql)

# disconnect from server
db.close()