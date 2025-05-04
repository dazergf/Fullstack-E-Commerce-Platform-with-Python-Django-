import mysql.connector as ryss

# Create your models here.

conn = ryss.connect(
        host='localhost',
        user='root',
        password='',
        database='myn'
    )

cursor = conn.cursor()

query = "select categorie_produit from produit group by categorie_produit"
cursor.execute(query)
cat = cursor.fetchall()

    
query = "select * from produit group by nom_produit"
cursor.execute(query)
produits = cursor.fetchall()

cursor.close()
conn.close()

