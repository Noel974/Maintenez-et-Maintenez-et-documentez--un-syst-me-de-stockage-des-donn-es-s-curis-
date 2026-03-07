import os
import sys
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# ==========================
#  CHARGEMENT CONFIGURATION
# ==========================

load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")

for var_name, value in {
    "CSV_FILE": CSV_FILE,
    "MONGO_DB_NAME": MONGO_DB_NAME,
    "MONGO_COLLECTION": MONGO_COLLECTION,
    "MONGO_URI": MONGO_URI
}.items():
    if not value:
        print(f"Erreur : variable {var_name} manquante dans .env")
        sys.exit(1)

if not os.path.exists(CSV_FILE):
    print(f"Erreur : le fichier CSV '{CSV_FILE}' est introuvable.")
    sys.exit(1)

# ==========================
#  CHARGEMENT DONNÉES
# ==========================

def load_csv(path):
    return pd.read_csv(path).fillna("NA")

def load_mongo(uri, db_name, collection):
    try:
        client = MongoClient(uri)
        data = list(client[db_name][collection].find({}, {"_id": 0}))
        client.close()
        return pd.DataFrame(data).fillna("NA")
    except Exception as e:
        print("Erreur connexion MongoDB :", e)
        sys.exit(1)

# ==========================
#  COMPARAISON
# ==========================

def compare(csv_df, mongo_df):

    # Vérif nombre de lignes
    if len(csv_df) != len(mongo_df):
        print("❌ Fichier non identique : nombre de lignes différent")
        print(f"CSV : {len(csv_df)} lignes | MongoDB : {len(mongo_df)} lignes")
        sys.exit(1)

    # Vérif colonnes
    if set(csv_df.columns) != set(mongo_df.columns):
        print("❌ Fichier non identique : colonnes différentes")
        print("Colonnes CSV :", set(csv_df.columns))
        print("Colonnes MongoDB :", set(mongo_df.columns))
        sys.exit(1)

    # Tri pour comparaison
    csv_sorted = csv_df.sort_values(by=list(csv_df.columns)).reset_index(drop=True)
    mongo_sorted = mongo_df.sort_values(by=list(mongo_df.columns)).reset_index(drop=True)

    # Vérif contenu
    if not csv_sorted.equals(mongo_sorted):
        print("❌ Fichier non identique : données différentes")
        sys.exit(1)

    print("✅ Les données CSV et MongoDB sont parfaitement identiques !")
    sys.exit(0)

# ==========================
#  MAIN
# ==========================

if __name__ == "__main__":
    csv_df = load_csv(CSV_FILE)
    mongo_df = load_mongo(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION)
    compare(csv_df, mongo_df)
