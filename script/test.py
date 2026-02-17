import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")

if not CSV_FILE:
    print("❌ Variable CSV_FILE non définie dans le .env")
    sys.exit(1)

# ==============================
# CONFIGURATION
# ==============================

EXPECTED_COLUMNS = {
    "Name": "object",
    "Age": "int64",
    "Gender": "object",
    "Blood Type": "object",
    "Medical Condition": "object",
    "Date of Admission": "object",
    "Doctor": "object",
    "Hospital": "object",
    "Insurance Provider": "object",
    "Billing Amount": "float64",
    "Room Number": "int64",
    "Admission Type": "object",
    "Discharge Date": "object",
    "Medication": "object",
    "Test Results": "object"
}

# ==============================
# FONCTIONS DE VALIDATION
# ==============================

def check_columns(df):
    print("\n--- Vérification des colonnes ---")
    missing = set(EXPECTED_COLUMNS.keys()) - set(df.columns)
    extra = set(df.columns) - set(EXPECTED_COLUMNS.keys())

    if missing:
        print("❌ Colonnes manquantes :", missing)
    else:
        print("✅ Toutes les colonnes obligatoires sont présentes")

    if extra:
        print("⚠️ Colonnes supplémentaires :", extra)


def check_types(df):
    print("\n--- Vérification des types ---")
    for col, expected_type in EXPECTED_COLUMNS.items():
        if col in df.columns:
            actual_type = str(df[col].dtype)
            if actual_type != expected_type:
                print(f"⚠️ Type différent pour {col} : {actual_type} (attendu : {expected_type})")
            else:
                print(f"✅ Type correct pour {col}")


def check_missing_values(df):
    print("\n--- Vérification des valeurs manquantes ---")
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            print(f"❌ {count} valeur(s) manquante(s) dans {col}")
        else:
            print(f"✅ Pas de valeur manquante dans {col}")


def check_duplicates(df):
    print("\n--- Vérification des doublons ---")
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"❌ {duplicates} ligne(s) en doublon détectée(s)")
    else:
        print("✅ Aucun doublon détecté")


def check_age_validity(df):
    if "Age" in df.columns:
        print("\n--- Vérification des âges ---")
        invalid_age = df[(df["Age"] < 0) | (df["Age"] > 120)]
        if len(invalid_age) > 0:
            print(f"❌ {len(invalid_age)} âge(s) invalide(s)")
        else:
            print("✅ Tous les âges sont plausibles")


# ==============================
# EXECUTION
# ==============================

def main():
    print("Chargement du fichier CSV...")

    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print("❌ Fichier introuvable :", CSV_FILE)
        sys.exit(1)
    except Exception as e:
        print("❌ Erreur lors du chargement :", e)
        sys.exit(1)

    print("Nombre de lignes :", len(df))
    print("Nombre de colonnes :", len(df.columns))

    check_columns(df)
    check_types(df)
    check_missing_values(df)
    check_duplicates(df)
    check_age_validity(df)

    print("\n✅ Analyse terminée")


if __name__ == "__main__":
    main()
