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

names_inserted = [doc["Name"] for doc in documents]

for doc in collection.find({"Name": {"$in": names_inserted}}, {"_id": 0}):
    print(doc)