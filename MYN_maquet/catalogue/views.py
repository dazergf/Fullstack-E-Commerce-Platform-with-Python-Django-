from django.shortcuts import redirect, render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector as conn
import catalogue.globals as a
from .models import solution,solution2
import marquet.views 


@csrf_exempt
def catalogue(request):
    return render(request,'catalogue/catalogue.html' ,{'clee':solution,'categorie':solution2})

@csrf_exempt
def panier(request):
    if request.GET.get('CONFIRMER_CATALOGUE')=='CONFIRMER' :
        id_PRODUIT= request.GET.getlist('produit')
    
        # Affichage des données
        post_items = request.POST.items()
        post_keys = request.POST.keys()
        post_values = request.POST.values()
        post_copy = request.POST.copy()
        post_copy['additional_key'] = 'Additional Value'

        connection=conn.connect(
            host='localhost',
            user='root',
            password='',
            database='myn',)
        cursor=connection.cursor()
        global _resultat
        _resultat= []             #la variable globale qui contient tous les produits selections par le client
        
        for i in id_PRODUIT:
            query = "select * from produit where ID_produit = %s "
            cursor.execute( query,(i,))
            resultat1=cursor.fetchall()
            _resultat.append(resultat1)

            
        somme = 0                               #pour la somme des prix des produits
        for i in _resultat:
            somme+=i[0][9]

        return render(request,'catalogue/panier.html' ,{'result':_resultat,'somme':somme})
    
    if request.method == 'GET' or request.method == "POST" and request.GET.get('CONFIRMER')== 'CONFIRMER':

        if   a.ID_CLIENT== 0: #variable pour recuperer l'ID_client
            return redirect('login') 
        
        else:
            connection=conn.connect(
            host='localhost',
            user='root',
            password='',
            database='myn',)
            cursor=connection.cursor()

            query="insert into commande(id_client) values(%s)"
            cursor.execute(query,(a.ID_CLIENT,))
            connection.commit()
            query="SELECT ID_commande FROM commande where ID_commande=(SELECT max(ID_commande)FROM commande)"
            cursor.execute(query)
            ID_cmd=cursor.fetchall()
            ID_commande_max=ID_cmd[0][0]             #recupere l'ID_commande maximum

            for i in _resultat:
                query="insert into details_commandes(ID_commande,id_produit) values(%s,%s)"
                cursor.execute(query,(ID_commande_max,i[0][0]))
                connection.commit()
            cursor.close()
            connection.close()        
            return render(request, 'reussi.html')







def search(request):
    if request.GET.get('Barre_de_recherche') == "":
        content=f"""<h1 style='text-align:center;background-color:black ;color:gray'> Pas de resultat pour cette recherche</h1><h2 style='color:red ;background-color:black;text-align:center;'> " {request.GET.get('Barre_de_recherche')} "</h2><h1>Non trouvé ⚠️⚠️</h1>"""
        return HttpResponse(content)
    else:
        connection = conn.connect(
        host='localhost',
        user='root',
        password='',
        database='myn',
        )
        cursor = connection.cursor()
        query="select * from produit group by nom_produit "
        cursor.execute(query)                                            # recupere tout les noms des elements dans BD
        rechercheList=cursor.fetchall()                                  #les stockes dans rechercheList

        recherche =request.GET.get('Barre_de_recherche').upper()        #recupere la valeur saisie dans la barre de recherche / upper()  pour la mettre majscule

        j=0
        nouvelleList=[]
        for i in rechercheList:
            j+=1
            i=list(i)                                               #convertit les tuples contenant chaque produit de la bd(ou de rechercheList)
            i[2]=i[2].upper()                                       #mettre tout les noms de rechercheList en majuscule
        
            if recherche in i[2]:
                nouvelleList.append(i)
        if nouvelleList ==[] :
            content=f"""<h1 style='text-align:center;background-color:black ;color:gray'> Pas de resultat pour cette recherche</h1><h2 style='color:red ;background-color:black ;text-align:center;'> "  {request.GET.get('Barre_de_recherche')}  "</h2><h1>Non trouvé⚠️/h1>"""
            return HttpResponse(content)
        return render(request, 'catalogue/search.html',{'element_trouve':nouvelleList})






       
  
        