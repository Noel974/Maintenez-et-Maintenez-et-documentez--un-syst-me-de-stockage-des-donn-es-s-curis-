import os
import sys
import time
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Import des fonctions de test
from test import main as test_csv_main
from testmigration import main as test_migration_main
from testcompare import compare_data, load_csv, load_mongodb

# ============================================================
#  CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
# ============================================================

load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD_RAW = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

required_vars = {
    "CSV_FILE": CSV_FILE,
    "MONGO_USER": MONGO_USER,
    "MONGO_PASSWORD": MONGO_PASSWORD_RAW,
    "MONGO_HOST": MONGO_HOST,
    "MONGO_PORT": MONGO_PORT,
    "MONGO_DB_NAME": MONGO_DB_NAME,
    "MONGO_COLLECTION": MONGO_COLLECTION
}

for var, value in required_vars.items():
    if not value:
        print(f"❌ ERREUR : La variable {var} n'est pas définie dans le fichier .env")
        sys.exit(1)

# Encodage identifiants
user = quote_plus(MONGO_USER)
password = quote_plus(MONGO_PASSWORD_RAW)

MONGO_URI = f"mongodb://{user}:{password}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"


# ============================================================
#  FONCTION GÉNÉRIQUE DE RETRY (compatible sys.exit)
# ============================================================

def run_with_retry(func, retries=3, delay=2):

    for attempt in range(1, retries + 1):
        print(f"\n🔁 Tentative {attempt}/{retries} pour : {func.__name__}")

        try:
            func()

            print(f"✅ Succès : {func.__name__}")
            return True

        except SystemExit as e:
            # Capture sys.exit()
            if e.code == 0:
                print(f"✅ Succès (code 0) : {func.__name__}")
                return True
            else:
                print(f"❌ Échec (code {e.code}) : {func.__name__}")

        except Exception as e:
            print(f"❌ Erreur technique lors de {func.__name__} : {e}")

        if attempt < retries:
            print(f"⏳ Nouvelle tentative dans {delay} seconde(s)...")
            time.sleep(delay)

    print(f"\n❌ Échec définitif après {retries} tentatives.")
    return False


# ============================================================
#  PIPELINE PRINCIPAL
# ============================================================

def main():

    print("\n==============================")
    print("    DÉMARRAGE DU PIPELINE")
    print("==============================\n")

    #  Test CSV
    print("=== TEST DU CSV (AVANT MIGRATION) ===")
    if not run_with_retry(test_csv_main):
        sys.exit(1)

    #  Test MongoDB après migration
    print("\n=== TEST DES DONNÉES DANS MONGODB (APRÈS MIGRATION) ===")
    if not run_with_retry(test_migration_main):
        sys.exit(1)

    #  Comparaison finale
    print("\n=== COMPARAISON CSV ↔ MONGODB ===")

    def compare_wrapper():
        csv_df = load_csv(CSV_FILE)
        mongo_df = load_mongodb(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION)
        compare_data(csv_df, mongo_df)

    if not run_with_retry(compare_wrapper):
        sys.exit(1)

    print("\n Pipeline exécuté avec succès ! Toutes les étapes sont validées.")
    sys.exit(0)


# ============================================================
#  POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    main()