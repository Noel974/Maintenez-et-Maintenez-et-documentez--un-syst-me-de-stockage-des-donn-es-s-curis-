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

print("=== MISE À JOUR DES PATIENTS ===")

updates = [
    {
        "filter": {"Name": "Ali Haddad"},
        "update": {"$set": {"Billing Amount": 4500.00}}
    },
    {
        "filter": {"Name": "Sara Benyahia"},
        "update": {"$set": {"Medical Condition": "Recovered"}}
    },
    {
        "filter": {"Name": "Karim Toumi"},
        "update": {"$set": {"Age": 48}}
    }
]

# UPDATE
count = 0
for u in updates:
    result = collection.update_one(u["filter"], u["update"])
    count += result.modified_count

print(f"✔ {count} patients mis à jour avec succès.")

# ==========================
# READ - afficher les patients mis à jour
# ==========================
print("\n=== LECTURE DES PATIENTS MIS À JOUR ===")

names_updated = [u["filter"]["Name"] for u in updates]

for doc in collection.find({"Name": {"$in": names_updated}}, {"_id": 0}):
    print(doc)

# Fermeture propre de la connexion
client.close()