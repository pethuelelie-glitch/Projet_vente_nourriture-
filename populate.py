import os
import sys
import django

sys.path.append(r'C:\Users\ELIE EHOUSSOU\Documents\PERSONNEL\Projet_Vente_nouriture\backend\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from products.models import Product

initial_products = [
    {"external_id": "garba", "name": "Attiéké Garba", "category": "attieke", "price": 1000, "image": "assets/images/garba.jpg", "description": "Attiéké accompagné de poisson, oignon, tomate et condiments."},
    {"external_id": "attieke-poisson", "name": "Attiéké + poisson braisé", "category": "attieke", "price": 1500, "image": "assets/images/attieke-poisson.jpg", "description": "Poisson braisé accompagné d'attiéké, d'oignon, tomate et condiments."},
    {"external_id": "attieke-poulet", "name": "Attiéké + poulet braisé", "category": "attieke", "price": 1500, "image": "assets/images/attieke-poulet.jpg", "description": "Poulet braisé accompagné d'attiéké et de ses garnitures."},
    {"external_id": "tchep-poulet", "name": "Tchèp au poulet", "category": "riz", "price": 1500, "image": "assets/images/tchep-poulet.jpg", "description": "Riz préparé avec légumes et poulet."},
    {"external_id": "tchep-poisson", "name": "Tchèp au poisson", "category": "riz", "price": 1500, "image": "assets/images/tchep-poisson.jpg", "description": "Riz préparé avec légumes et poisson."},
]

for p_data in initial_products:
    Product.objects.get_or_create(external_id=p_data['external_id'], defaults=p_data)

print("Produits ajoutes avec succes !")
