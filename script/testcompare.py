import os
import sys
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# ==========================
# 1️⃣ CHARGEMENT CONFIGURATION (.env)
# ==========================

load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")

# Vérification variables obligatoires
required_vars = {
    "CSV_FILE": CSV_FILE,
    "MONGO_DB_NAME": MONGO_DB_NAME,
    "MONGO_COLLECTION": MONGO_COLLECTION,
    "MONGO_URI": MONGO_URI
}

for var_name, value in required_vars.items():
    if not value:
        print(f"❌ Variable {var_name} non définie dans le .env")
        sys.exit(1)

# Vérification existence fichier CSV
if not os.path.exists(CSV_FILE):
    print(f"❌ Le fichier {CSV_FILE} n'existe pas.")
    sys.exit(1)

print("✔ Configuration chargée avec succès")

# ==========================
# 2️⃣ CHARGEMENT DONNÉES
# ==========================

def load_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df


def load_mongodb(uri, MONGO_DB_NAME, MONGO_COLLECTION):
    client = MongoClient(uri)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION]

    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)

    return df


# ==========================
# 3️⃣ COMPARAISON
# ==========================

def compare_data(csv_df, mongo_df):

    print("\n=== COMPARAISON CSV vs MONGODB ===")

    # Harmoniser valeurs manquantes
    csv_df = csv_df.fillna("NA")
    mongo_df = mongo_df.fillna("NA")

    # 1️⃣ Nombre de lignes
    print("\nNombre de lignes :")
    print("CSV :", len(csv_df))
    print("MongoDB :", len(mongo_df))

    if len(csv_df) == len(mongo_df):
        print("✔ Même nombre de lignes")
    else:
        print("❌ Nombre de lignes différent")

    # 2️⃣ Colonnes
    if set(csv_df.columns) == set(mongo_df.columns):
        print("✔ Colonnes identiques")
    else:
        print("❌ Colonnes différentes")
        print("CSV :", set(csv_df.columns))
        print("MongoDB :", set(mongo_df.columns))

    # 3️⃣ Comparaison complète
    try:
        csv_sorted = csv_df.sort_values(by=list(csv_df.columns)).reset_index(drop=True)
        mongo_sorted = mongo_df.sort_values(by=list(mongo_df.columns)).reset_index(drop=True)

        if csv_sorted.equals(mongo_sorted):
            print("\n✔ Les données sont STRICTEMENT identiques")
        else:
            print("\n❌ Les données sont différentes")
    except Exception as e:
        print("Erreur lors de la comparaison :", e)


# ==========================
# 4️⃣ MAIN
# ==========================

if __name__ == "__main__":

    csv_df = load_csv(CSV_FILE)
    mongo_df = load_mongodb(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION)

    compare_data(csv_df, mongo_df)
