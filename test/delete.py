from pymongo import MongoClient
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Charger configuration
load_dotenv()

# Récupération des variables d'environnement
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
CSV_FILE = os.getenv("CSV_FILE")

# Vérification des variables obligatoires
required_vars = {
    "MONGO_USER": MONGO_USER,
    "MONGO_PASSWORD": MONGO_PASSWORD,
    "MONGO_DB_NAME": MONGO_DB_NAME,
    "MONGO_COLLECTION": MONGO_COLLECTION,
    "CSV_FILE": CSV_FILE,
}

missing = [k for k, v in required_vars.items() if not v]
if missing:
    raise ValueError(f"Variables d'environnement manquantes : {', '.join(missing)}")

# Encodage des identifiants
user = quote_plus(MONGO_USER)
password = quote_plus(MONGO_PASSWORD)

# URI MongoDB
MONGO_URI = f"mongodb://{user}:{password}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION]

print("✅ Connexion à MongoDB réussie.")

print("=== SUPPRESSION DES 5 PATIENTS ===")

patients_to_delete = [
    "Ali Haddad",
    "Sara Benyahia",
    "Karim Toumi",
    "Lina Mansouri",
    "Nadia Khelifi"
]

# DELETE
result = collection.delete_many({"Name": {"$in": patients_to_delete}})

print(f"✔ {result.deleted_count} patients supprimés avec succès.")

# Fermeture de la connexion
client.close()