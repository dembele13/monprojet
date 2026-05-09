from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBConnection:
    """Gestionnaire de connexion MongoDB"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        try:
            self.client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                retryWrites=True,
                tz_aware=True,
            )
            # Test la connexion
            self.client.admin.command('ismaster')
            self.db = self.client[settings.MONGODB_DB_NAME]
            logger.info(f"✅ MongoDB connecté à {settings.MONGODB_DB_NAME}")
            self._initialized = True
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            logger.error(f"❌ Erreur connexion MongoDB: {e}")
            raise

def get_db():
    """Obtenir la base de données MongoDB"""
    connection = MongoDBConnection()
    return connection.db

def get_collection(name):
    """Obtenir une collection MongoDB"""
    db = get_db()
    return db[name]

def close_connection():
    """Fermer la connexion MongoDB"""
    connection = MongoDBConnection()
    connection.client.close()
    logger.info("Connexion MongoDB fermée")