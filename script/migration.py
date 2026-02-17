import os
import csv
from pymongo import MongoClient
from dotenv import load_dotenv


def convert_value(value):
    """Convertit automatiquement les types (int, float, None)."""
    if value == "":
        return None

    # Tentative int
    try:
        return int(value)
    except ValueError:
        pass

    # Tentative float
    try:
        return float(value)
    except ValueError:
        pass

    # Sinon string
    return value


def main():
    client = None

    try:
        # Charger les variables d'environnement
        load_dotenv()

        MONGO_URI = os.getenv("MONGO_URI")
        MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
        MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
        CSV_FILE = os.getenv("CSV_FILE")

        if not all([MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION, CSV_FILE]):
            raise ValueError("Une ou plusieurs variables d'environnement sont manquantes.")

        # Connexion MongoDB
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION]

        print("✅ Connexion à MongoDB réussie.")

        # Vérifier que le fichier existe
        if not os.path.exists(CSV_FILE):
            raise FileNotFoundError(f"Fichier introuvable : {CSV_FILE}")

        records = []

        # Lecture du CSV
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                clean_row = {key: convert_value(value) for key, value in row.items()}
                records.append(clean_row)

        if not records:
            print("⚠️ Le fichier CSV est vide.")
            return

        # Insertion MongoDB
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
