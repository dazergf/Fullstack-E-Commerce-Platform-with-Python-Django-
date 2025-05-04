from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import cat, produits
import mysql.connector
import catalogue.globals as a
from catalogue.views import panier

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom_client = request.POST['nom_client']
        prenom_client = request.POST['prenom_client']
        numero_telephone_client = request.POST['numero_telephone_client']
        sexe_client = request.POST['sexe_client']
        age_client = request.POST['age_client']
        ville_client = request.POST['ville_client']
        district_client = request.POST['district_client']
        quartier_client = request.POST['quartier_client']
        numero_parselle_client = request.POST['numero_parselle_client']
        mot_de_passe_client = request.POST['mot_de_passe_client']
        reponse_de_securite_client = request.POST['reponse_de_securite_client']
        e_mail_client = request.POST['e_mail_client']
        rue_ou_avenue_client = request.POST['rue_ou_avenue_client']

        # Connecter à la base de données MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='myn'
        )
        cursor = conn.cursor()

        # Insérer les données dans la table `client`
        query = """
        INSERT INTO client (
            Nom_client, prenom_client, numero_telephonne_client, sexe_client, age_client,
            ville_client, district_client, quartier_client, numero_parselle_client,
            mot_de_passe_client, reponse_de_securite_client, e_mail_client, rue_ou_avenue_client
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            nom_client, prenom_client, numero_telephone_client, sexe_client, age_client,
            ville_client, district_client, quartier_client, numero_parselle_client,
            mot_de_passe_client, reponse_de_securite_client, e_mail_client, rue_ou_avenue_client
        )
        cursor.execute(query, values)
        conn.commit()
#_____________________________ajouté____________________________________
        query = "select max(id_client) from client"     # recuperation p l'id de l'utilisateur qui vient de s'inscrire
        cursor.execute(query)                           # ***********
        user = cursor.fetchone()                       #**************
#_______________________________________________________________________
        cursor.close()
        conn.close()

        if user and user[0] is not None:
            #Utilisateur trouvé, rediriger vers une page de succès par exemple
            a.ID_CLIENT = user[0]                      # variable de l'id du lient connecter
        return redirect('home')  # Redirigez vers une page de succès après l'inscription

    return render(request, 'inscription.html')



#definition de vue de connection
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('Mot_De_passe')

        # Connexion à la base de données MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='myn'
        )
        cursor = conn.cursor()

        # Vérifier si l'utilisateur existe dans la base de données
        query = "SELECT * FROM client WHERE e_mail_client = %s AND mot_de_passe_client = %s"
        cursor.execute(query, (email, mot_de_passe))
        user = cursor.fetchone()  # Récupère une seule ligne correspondant à l'utilisateur

        cursor.close()
        conn.close()

        if user:
            # Utilisateur trouvé, rediriger vers une page de succès par exemple
            a.ID_CLIENT = user[0]
            return redirect('home')  # Assurez-vous d'avoir défini cette URL dans urls.py
        else:
            # Utilisateur non trouvé, rediriger vers une page d'échec de connexion par exemple
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect")  # Affichez à nouveau le formulaire de connexion avec un message d'erreur si nécessaire

    # Si la méthode HTTP n'est pas POST, affichez simplement le formulaire de connexion
    return render(request, 'connexion.html')


#definition de vue des info de mon compte
def mon_compte(request):
    user_id = a.ID_CLIENT
    if not user_id:
        return redirect('login')  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté

    # Connexion à la base de données MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='myn'
    )
    cursor = conn.cursor()

    # Récupérer les informations de l'utilisateur
    query = "SELECT * FROM client WHERE id_client = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    query= "SELECT * from commande where id_client=%s"
    cursor.execute(query, (user_id,))
    commande_client = cursor.fetchall()

    
    detail_client=[]
    for i in commande_client:
        id_CMD = i[0]

        query= "SELECT produit.nom_produit,produit.TTC_produit, details_commandes.ID_commande from details_commandes inner join produit ON produit.ID_produit=details_commandes.ID_produit where ID_commande=%s"
        cursor.execute(query, (id_CMD,))
        detail_client.append(cursor.fetchall())

    
    print('*'*10)
    print(commande_client)
    print(detail_client)
   
    cursor.close()
    conn.close()     

    if user:
       user_dict = {
           'id_client': user[0],
            'Nom_client': user[1],
            'prenom_client': user[2],
            'telephonne': user[3],
            'sexe_client': user[4],
            'age_client': user[5],
            'ville_client': user[6],
            'district': user[7],
            'quartier_client': user[8],
            'parselle': user[9],
            'mot_de_passe': user[10],               
            'e_mail_client': user[12],
            'rue': user[13],
        }

    return render(request, 'mon_compte.html', {'CMD':commande_client, 'detail':detail_client, 'user': user_dict})

    

#definition de la page d'aceuil mynweb
@csrf_exempt
def acceuil(request):
    a.ID_CLIENT=0

    # vue pour le racourcie des produit _________________________________________________
    if request.method == 'POST':
        print("POST"*1000)
        id_PRODUIT= request.POST.getlist('produit')
       

        # Affichage des données
        post_items = request.POST.items()
        post_keys = request.POST.keys()
        post_values = request.POST.values()
        post_copy = request.POST.copy()
        post_copy['additional_key'] = 'Additional Value'
        #print(id_PRODUIT)

        connection=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='myn',)
        cursor=connection.cursor()
        #global  _resultat                    #la viriable globale qui contient tous les produits selections par le client
        #_resultat= []
        print(a._resultat)
        for i in id_PRODUIT:
            query = "select * from produit where ID_produit = %s "
            cursor.execute( query,(i,))
            resultat1=cursor.fetchall()
            a._resultat.append(resultat1)
        return redirect(panier)
    
    # Passer les données au template
    #affihage des produits et cat______________________________________________
    return render(request, 'acceuil.html', {'categorie': cat, 'produit': produits})




#definition de la page home quand l'utilisateur est connecter sur notre site
@csrf_exempt
def home(request):
    user_id = a.ID_CLIENT
    print(user_id)
    if not user_id or user_id == 0:       #j'ai aujouter ça___________________________________________
        return redirect('login')

    conn = mysql.connector.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'myn'
    )
    cursor = conn.cursor()

    query = "select * from client where id_client = %s"     #requete pour recuperer l'id client
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        user_dict = {
           
            'Nom_client': user[1],
            'prenom_client': user[2],
        }

    else:
        user_dict = {}

    
    #context combiné pour l'affichage
    context = {
        'user': user_dict,
        'categorie': cat,         # Assurez-vous que 'cat' et 'produits' sont définis et valides.
        'produit': produits
    }

     # vue pour le racourcie des produit sur la page home_________________________________________________
    if request.method == 'POST':
        print("POST"*1000)
        id_PRODUIT= request.POST.getlist('produit')
       

        # Affichage des données
        post_items = request.POST.items()
        post_keys = request.POST.keys()
        post_values = request.POST.values()
        post_copy = request.POST.copy()
        post_copy['additional_key'] = 'Additional Value'
        #print(id_PRODUIT)

        connection=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='myn',)
        cursor=connection.cursor()
        #global  _resultat                    #la viriable globale qui contient tous les produits selections par le client
        #_resultat= []
        
        for i in id_PRODUIT:
            query = "select * from produit where ID_produit = %s "
            cursor.execute( query,(i,))
            resultat1=cursor.fetchall()
            a._resultat.append(resultat1)
        return redirect(panier)

    return render(request, 'home.html', context)

def reussi(request):
    return render(request, 'reussi.html')