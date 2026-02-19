import os
from test import main as test_csv_main
from testmigration import main as test_migration_main
from testcompare import compare_data, load_csv, load_mongodb
from dotenv import load_dotenv

# Charger variables d'environnement
load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")

def main():
    print("=== TEST AUTOMATIQUE AVANT MIGRATION (CSV) ===")
    # Si test.py main() accepte un argument CSV, on le passe
    test_csv_main()

    print("\n=== TEST AUTOMATIQUE APRÈS MIGRATION (MongoDB) ===")
    test_migration_main()

    print("\n=== COMPARAISON AUTOMATIQUE CSV ↔ MongoDB ===")
    # Charger CSV et MongoDB avec les bons arguments
    csv_df = load_csv(CSV_FILE)
    mongo_df = load_mongodb(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION)

    compare_data(csv_df, mongo_df)

if __name__ == "__main__":
    main()
