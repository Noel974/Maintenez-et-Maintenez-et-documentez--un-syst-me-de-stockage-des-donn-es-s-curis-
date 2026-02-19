from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Charger configuration
load_dotenv()

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")

# Vérification variables obligatoires
required_vars = {
    "MONGO_DB_NAME": MONGO_DB_NAME,
    "MONGO_COLLECTION": MONGO_COLLECTION,
    "MONGO_URI": MONGO_URI
}

missing = [k for k, v in required_vars.items() if not v]
if missing:
    raise ValueError(f"Variables d'environnement manquantes : {', '.join(missing)}")

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION]

print("=== INSERTION DE 5 DOCUMENTS ===")

documents = [
    {
        "Name": "Ali Haddad",
        "Age": 52,
        "Gender": "Male",
        "Blood Type": "O+",
        "Medical Condition": "Diabetes",
        "Billing Amount": 4200.75
    },
    {
        "Name": "Sara Benyahia",
        "Age": 34,
        "Gender": "Female",
        "Blood Type": "A-",
        "Medical Condition": "Hypertension",
        "Billing Amount": 3100.00
    },
    {
        "Name": "Karim Toumi",
        "Age": 47,
        "Gender": "Male",
        "Blood Type": "B+",
        "Medical Condition": "Asthma",
        "Billing Amount": 2800.50
    },
    {
        "Name": "Lina Mansouri",
        "Age": 29,
        "Gender": "Female",
        "Blood Type": "AB+",
        "Medical Condition": "Fracture",
        "Billing Amount": 5100.20
    },
    {
        "Name": "Nadia Khelifi",
        "Age": 60,
        "Gender": "Female",
        "Blood Type": "O-",
        "Medical Condition": "Heart Disease",
        "Billing Amount": 7800.00
    }
]

# CREATE
result = collection.insert_many(documents)
print(f"✔ {len(result.inserted_ids)} documents insérés avec succès.")

# ==========================
# READ - afficher les documents insérés
# ==========================
print("\n=== LECTURE DES DOCUMENTS INSÉRÉS ===")

# On filtre pour afficher uniquement les documents qu'on vient d'insérer
names_inserted = [doc["Name"] for doc in documents]

for doc in collection.find({"Name": {"$in": names_inserted}}, {"_id": 0}):
    print(doc)
