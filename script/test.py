import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")

if not CSV_FILE:
    print(" Variable CSV_FILE non définie dans le .env")
    sys.exit(1)

# ==============================
# CONFIGURATION
# ==============================

EXPECTED_COLUMNS = {
    "Name": "str",
    "Age": "int64",
    "Gender": "str",
    "Blood Type": "str",
    "Medical Condition": "str",
    "Date of Admission": "str",
    "Doctor": "str",
    "Hospital": "str",
    "Insurance Provider": "str",
    "Billing Amount": "float64",
    "Room Number": "int64",
    "Admission Type": "str",
    "Discharge Date": "str",
    "Medication": "str",
    "Test Results": "str"
}

# ==============================
# FONCTIONS DE VALIDATION
# ==============================

def check_columns(df):
    print("\n--- Vérification des colonnes ---")
    missing = set(EXPECTED_COLUMNS.keys()) - set(df.columns)
    extra = set(df.columns) - set(EXPECTED_COLUMNS.keys())

    critical_error = False

    if missing:
        print(" Colonnes manquantes :")
        for col in missing:
            print(f"   - {col}")
        critical_error = True
    else:
        print(" Toutes les colonnes obligatoires sont présentes")

    if extra:
        print(f"\n {len(extra)} colonne(s) supplémentaire(s) détectée(s) :")
        for col in extra:
            print(f"   - {col}")
        print(" Ces colonnes ne sont pas attendues dans la configuration.")
        critical_error = True
    else:
        print(" Aucune colonne supplémentaire détectée")

    return critical_error


def check_types(df):
    print("\n--- Vérification des types ---")
    critical_error = False

    for col, expected_type in EXPECTED_COLUMNS.items():
        if col in df.columns:
            actual_type = str(df[col].dtype)
            if actual_type != expected_type:
                print(f" Type incorrect pour {col} : {actual_type} (attendu : {expected_type})")
                critical_error = True
            else:
                print(f" Type correct pour {col}")

    return critical_error


def check_missing_values(df):
    print("\n--- Vérification des valeurs manquantes ---")
    missing = df.isnull().sum()

    for col, count in missing.items():
        if count > 0:
            print(f" {count} valeur(s) manquante(s) dans {col}")
        else:
            print(f" Pas de valeur manquante dans {col}")


def check_duplicates(df):
    print("\n--- Vérification des doublons ---")
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        print(f" {duplicates} ligne(s) en doublon détectée(s)")
    else:
        print(" Aucun doublon détecté")


def check_age_validity(df):
    print("\n--- Vérification des âges ---")
    critical_error = False

    if "Age" in df.columns:
        invalid_age = df[(df["Age"] < 0) | (df["Age"] > 120)]

        if len(invalid_age) > 0:
            print(f" {len(invalid_age)} âge(s) invalide(s)")
            critical_error = True
        else:
            print(" Tous les âges sont plausibles")

    return critical_error


# ==============================
# EXECUTION
# ==============================

def main():
    print("Chargement du fichier CSV...")

    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(" Fichier introuvable :", CSV_FILE)
        sys.exit(1)
    except Exception as e:
        print(" Erreur lors du chargement :", e)
        sys.exit(1)

    print("Nombre de lignes :", len(df))
    print("Nombre de colonnes :", len(df.columns))

    errors = False

    # Vérifications critiques
    if check_columns(df):
        errors = True

    if check_types(df):
        errors = True

    if check_age_validity(df):
        errors = True

    # Vérifications informatives
    check_missing_values(df)
    check_duplicates(df)

    print("\n--- Résultat final ---")

    if errors:
        print(" Erreurs critiques détectées. Arrêt du programme.")
        sys.exit(1)
    else:
        print(" Validation réussie. Aucune erreur critique.")
        sys.exit(0)


if __name__ == "__main__":
    main()