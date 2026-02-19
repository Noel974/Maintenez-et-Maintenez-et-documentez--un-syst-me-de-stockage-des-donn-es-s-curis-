from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Charger configuration
load_dotenv()

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION]

print("=== SUPPRESSION DES 5 PATIENTS ===")

patients_to_delete = [
    "Ali Haddad",
    "Sara Benyahia",
    "Karim Toumi",
    "Lina Mansouri",
    "Nadia Khelifi"
]

result = collection.delete_many({"Name": {"$in": patients_to_delete}})

print(f"✔ {result.deleted_count} patients supprimés avec succès.")
