import mysql.connector as conn

connection=conn.connect(
        host='localhost',
        user='root',
        password='',
        database='myn',)
    

cursor=connection.cursor()
cursor.execute(" select  * from produit group by nom_produit ")    
solution=cursor.fetchall()
cursor.execute("SELECT categorie_produit FROM produit GROUP by categorie_produit")
solution2=cursor.fetchall()
#print(solution)
cursor.close()
connection.disconnect()