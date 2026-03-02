from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pymongo import MongoClient
from django.conf import settings
from .models import Enseignant, Cours, Etudiant

# Connexion MongoDB (configuration dans settings.py)
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB_NAME]

# Collections MongoDB pour chaque modèle
collection_enseignant = db['enseignants']
collection_cours = db['cours']
collection_etudiant = db['etudiants']

def model_to_dict(instance):
    """Convertit une instance Django en dictionnaire (sans champ '_state')"""
    data = instance.__dict__.copy()
    data.pop('_state', None)
    # Gestion des relations (ex: ManyToMany) - on les ignore pour la synchro simple
    return data

@receiver(post_save, sender=Enseignant)
def sync_enseignant_to_mongo(sender, instance, **kwargs):
    data = model_to_dict(instance)
    collection_enseignant.update_one(
        {'idens': instance.idens},
        {'$set': data},
        upsert=True
    )

@receiver(post_save, sender=Cours)
def sync_cours_to_mongo(sender, instance, **kwargs):
    data = model_to_dict(instance)
    # On remplace l'objet enseignant par son ID pour éviter la complexité
    if instance.enseignant_id:
        data['enseignant_id'] = instance.enseignant_id
    collection_cours.update_one(
        {'idcours': instance.idcours},
        {'$set': data},
        upsert=True
    )

@receiver(post_save, sender=Etudiant)
def sync_etudiant_to_mongo(sender, instance, **kwargs):
    data = model_to_dict(instance)
    # Les ManyToMany ne sont pas inclus dans __dict__, on les ajoute si besoin
    data['cours_ids'] = list(instance.cours.values_list('idcours', flat=True))
    collection_etudiant.update_one(
        {'idetu': instance.idetu},
        {'$set': data},
        upsert=True
    )

# Optionnel : suppression dans MongoDB quand un objet est supprimé dans SQLite
@receiver(post_delete, sender=Enseignant)
def delete_enseignant_from_mongo(sender, instance, **kwargs):
    collection_enseignant.delete_one({'idens': instance.idens})

@receiver(post_delete, sender=Cours)
def delete_cours_from_mongo(sender, instance, **kwargs):
    collection_cours.delete_one({'idcours': instance.idcours})

@receiver(post_delete, sender=Etudiant)
def delete_etudiant_from_mongo(sender, instance, **kwargs):
    collection_etudiant.delete_one({'idetu': instance.idetu})