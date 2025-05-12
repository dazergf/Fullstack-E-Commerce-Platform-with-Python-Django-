from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import cat, produits
import mysql.connector
import catalogue.globals as a
from catalogue.views import panier


#definition de vue de connection
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('e_mail_client')
        mot_de_passe = request.POST.get('mot_de_passe_client')

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

        

        if user:
            request.session['userID'] = user[0]
            request.session['nom_client'] = user[1]
            request.session['prenom_client'] = user[2]            
            if request.session.get('previous_url'):
                previous_url = request.session.pop('previous_url')
                return redirect(previous_url)
            return redirect('home')  # Assurez-vous d'avoir défini cette URL dans urls.py
        else:
            # Utilisateur non trouvé, rediriger vers une page d'échec de connexion par exemple
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect")  # Affichez à nouveau le formulaire de connexion avec un message d'erreur si nécessaire

    # Si la méthode HTTP n'est pas POST, affichez simplement le formulaire de connexion
    return render(request, 'connexion.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom_client = request.POST['nom_client']
        prenom_client = request.POST['prenom_client']
        mot_de_passe_client = request.POST['mot_de_passe_client']
        e_mail_client = request.POST['e_mail_client']

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
            Nom_client,
            prenom_client,
            mot_de_passe_client, 
            e_mail_client
        ) VALUES (%s, %s, %s, %s)
        """
        values = (
            nom_client,
            prenom_client, 
            mot_de_passe_client, 
            e_mail_client
        )
        cursor.execute(query, values)
        conn.commit()
        return login(request)

    return render(request, 'inscription.html')


#definition de vue des info de mon compte
def mon_compte(request):
    user_id = request.session.get('userID')
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

   
    cursor.close()
    conn.close()     

    if user:
       user_dict = {
           'id_client': user[0],
            'Nom_client': user[1],
            'prenom_client': user[2],
            'telephonne': user[3],
            'mot_de_passe': user[10],               
            'e_mail_client': user[12],
            'rue': user[13],
        }

    return render(request, 'mon_compte.html', {'CMD':commande_client, 'detail':detail_client, 'user': user_dict})

    

#definition de la page d'aceuil mynweb
@csrf_exempt
def accueil(request):
    return render(request, 'acceuil.html')




#definition de la page home quand l'utilisateur est connecter sur notre site
@csrf_exempt
def home(request):
    user_id = request.session['userID'] 

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
def logout(request):
    request.session.flush()  # Supprime toutes les données de session
    return redirect('accueil')  # Redirigez vers la page d'accueil ou de connexion

def service_client(request):
    return render(request,'service_client.html')  
def livraison(request):
    return render(request,'livraison.html')  