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

print("=== MISE À JOUR DE 3 PATIENTS ===")

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

count = 0
for u in updates:
    result = collection.update_one(u["filter"], u["update"])
    count += result.modified_count

print(f"✔ {count} patients mis à jour avec succès.")

# ==========================
# READ - afficher les patients mis à jour
# ==========================
print("\n=== LECTURE DES PATIENTS MIS À JOUR ===")

# On récupère les noms des patients mis à jour
names_updated = [u["filter"]["Name"] for u in updates]

for doc in collection.find({"Name": {"$in": names_updated}}, {"_id": 0}):
    print(doc)
