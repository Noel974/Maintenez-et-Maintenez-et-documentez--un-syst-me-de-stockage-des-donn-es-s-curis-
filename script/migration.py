import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus


def main():
    client = None  # Pour éviter une erreur dans le finally

    try:
        # Charger les variables d'environnement
        load_dotenv()

        MONGO_USER = os.getenv("MONGO_USER")
        MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
        MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
        MONGO_PORT = os.getenv("MONGO_PORT", "27017")
        MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
        MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
        CSV_FILE = os.getenv("CSV_FILE")

        if not all([MONGO_USER, MONGO_PASSWORD, MONGO_DB_NAME, MONGO_COLLECTION, CSV_FILE]):
            raise ValueError("Une ou plusieurs variables d'environnement sont manquantes.")

        # Encodage des identifiants
        user = quote_plus(MONGO_USER)
        password = quote_plus(MONGO_PASSWORD)

        MONGO_URI = f"mongodb://{user}:{password}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"

        # Connexion MongoDB
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION]

        print("✅ Connexion à MongoDB réussie.")

        # Lecture CSV
        df = pd.read_csv(CSV_FILE)

        if df.empty:
            print("⚠️ Le fichier CSV est vide.")
            return

        # Remplacer les NaN par None (important pour MongoDB)
        df = df.where(pd.notnull(df), None)

        records = df.to_dict(orient="records")

        # Insertion
        result = collection.insert_many(records)
        print(f"✅ {len(result.inserted_ids)} documents insérés avec succès.")

    except Exception as e:
        print("❌ Erreur :", e)

    finally:
        if client:
            client.close()
            print("🔒 Connexion MongoDB fermée.")


if __name__ == "__main__":
    main()