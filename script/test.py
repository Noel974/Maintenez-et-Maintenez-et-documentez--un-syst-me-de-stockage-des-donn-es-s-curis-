import csv
import sys

CSV_FILE = "data/healthcare_dataset.csv"

# ==============================
# CONFIGURATION
# ==============================

EXPECTED_COLUMNS = {
    "Name": "object",
    "Age": "int",
    "Gender": "object",
    "Blood Type": "object",
    "Medical Condition": "object",
    "Date of Admission": "object",
    "Doctor": "object",
    "Hospital": "object",
    "Insurance Provider": "object",
    "Billing Amount": "float",
    "Room Number": "int",
    "Admission Type": "object",
    "Discharge Date": "object",
    "Medication": "object",
    "Test Results": "object"
}

# ==============================
# FONCTIONS DE VALIDATION
# ==============================

def check_columns(header):
    print("\n--- Vérification des colonnes ---")
    missing = set(EXPECTED_COLUMNS.keys()) - set(header)
    extra = set(header) - set(EXPECTED_COLUMNS.keys())

    if missing:
        print("❌ Colonnes manquantes :", missing)
    else:
        print("✅ Toutes les colonnes obligatoires sont présentes")

    if extra:
        print("⚠️ Colonnes supplémentaires :", extra)


def convert_value(value, expected_type):
    if expected_type == "int":
        try:
            return int(value)
        except:
            return None
    if expected_type == "float":
        try:
            return float(value)
        except:
            return None
    return value  # object → string


def check_types(rows):
    print("\n--- Vérification des types ---")
    for col, expected_type in EXPECTED_COLUMNS.items():
        incorrect = 0
        for row in rows:
            value = row[col]
            converted = convert_value(value, expected_type)
            if converted is None and value != "":
                incorrect += 1

        if incorrect > 0:
            print(f"⚠️ Type incorrect dans {col} : {incorrect} valeur(s) invalide(s)")
        else:
            print(f"✅ Type correct pour {col}")


def check_missing_values(rows):
    print("\n--- Vérification des valeurs manquantes ---")
    missing_counts = {col: 0 for col in EXPECTED_COLUMNS}

    for row in rows:
        for col in EXPECTED_COLUMNS:
            if row[col] == "" or row[col] is None:
                missing_counts[col] += 1

    for col, count in missing_counts.items():
        if count > 0:
            print(f"❌ {count} valeur(s) manquante(s) dans {col}")
        else:
            print(f"✅ Pas de valeur manquante dans {col}")


def check_duplicates(rows):
    print("\n--- Vérification des doublons ---")
    seen = set()
    duplicates = 0

    for row in rows:
        row_tuple = tuple(row.items())
        if row_tuple in seen:
            duplicates += 1
        else:
            seen.add(row_tuple)

    if duplicates > 0:
        print(f"❌ {duplicates} ligne(s) en doublon détectée(s)")
    else:
        print("✅ Aucun doublon détecté")


def check_age_validity(rows):
    print("\n--- Vérification des âges ---")
    invalid = 0

    for row in rows:
        try:
            age = int(row["Age"])
            if age < 0 or age > 120:
                invalid += 1
        except:
            invalid += 1

    if invalid > 0:
        print(f"❌ {invalid} âge(s) invalide(s)")
    else:
        print("✅ Tous les âges sont plausibles")


# ==============================
# EXECUTION
# ==============================

def main():
    print("Chargement du fichier CSV...")

    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames
            rows = list(reader)

    except FileNotFoundError:
        print("❌ Fichier introuvable :", CSV_FILE)
        sys.exit(1)
    except Exception as e:
        print("❌ Erreur lors du chargement :", e)
        sys.exit(1)

    print("Nombre de lignes :", len(rows))
    print("Nombre de colonnes :", len(header))

    check_columns(header)
    check_types(rows)
    check_missing_values(rows)
    check_duplicates(rows)
    check_age_validity(rows)

    print("\n✅ Analyse terminée")


if __name__ == "__main__":
    main()
