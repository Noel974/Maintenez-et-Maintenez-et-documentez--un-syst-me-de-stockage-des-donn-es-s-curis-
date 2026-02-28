import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

EXPECTED_FIELDS = {
    "Name": str,
    "Age": int,
    "Gender": str,
    "Blood Type": str,
    "Medical Condition": str,
    "Date of Admission": str,
    "Doctor": str,
    "Hospital": str,
    "Insurance Provider": str,
    "Billing Amount": float,
    "Room Number": int,
    "Admission Type": str,
    "Discharge Date": str,
    "Medication": str,
    "Test Results": str
}


def main():
    load_dotenv()

    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

    if not MONGO_URI or not MONGO_DB_NAME or not MONGO_COLLECTION:
        print(" Variables d'environnement MongoDB manquantes.")
        sys.exit(1)

    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION]
    except Exception as e:
        print(" Erreur de connexion à MongoDB :", e)
        sys.exit(1)

    print("Lecture des données depuis MongoDB...")
    documents = list(collection.find({}, {"_id": 0}))

    if not documents:
        print(" Aucune donnée trouvée.")
        sys.exit(1)

    print(f"Nombre de documents : {len(documents)}")

    errors = False

    # ==============================
    # Vérification des colonnes
    # ==============================

    print("\n--- Vérification des colonnes ---")

    all_keys = set()
    for doc in documents:
        all_keys.update(doc.keys())

    missing = set(EXPECTED_FIELDS.keys()) - all_keys
    extra = all_keys - set(EXPECTED_FIELDS.keys())

    if missing:
        print(" Colonnes manquantes :")
        for field in missing:
            print(f"   - {field}")
        errors = True
    else:
        print(" Toutes les colonnes obligatoires sont présentes")

    if extra:
        print(f" {len(extra)} colonne(s) supplémentaire(s) détectée(s) :")
        for field in extra:
            print(f"   - {field}")
        errors = True
    else:
        print(" Aucune colonne supplémentaire détectée")
    # ==============================
    # Vérification des types
    # ==============================

    print("\n--- Vérification des types ---")

    for field, expected_type in EXPECTED_FIELDS.items():
        for doc in documents:
            if field in doc and doc[field] is not None:
                if not isinstance(doc[field], expected_type):
                    print(f" Mauvais type pour {field} : {type(doc[field])} (attendu : {expected_type})")
                    errors = True
                    break
        else:
            print(f" Type correct pour {field}")

    # ==============================
    # Valeurs manquantes (warning)
    # ==============================

    print("\n--- Vérification des valeurs manquantes ---")

    for field in EXPECTED_FIELDS.keys():
        missing_count = sum(
            1 for doc in documents
            if field not in doc or doc[field] is None
        )
        if missing_count > 0:
            print(f" {missing_count} valeur(s) manquante(s) dans {field}")
        else:
            print(f" Pas de valeur manquante dans {field}")

    # ==============================
    # Doublons (warning)
    # ==============================

    print("\n--- Vérification des doublons ---")

    doc_tuples = [tuple(sorted(doc.items())) for doc in documents]
    duplicates = len(doc_tuples) - len(set(doc_tuples))

    if duplicates > 0:
        print(f" {duplicates} doublon(s) détecté(s)")
    else:
        print(" Aucun doublon détecté")

    # ==============================
    # Validité des âges
    # ==============================

    print("\n--- Vérification des âges ---")

    invalid_ages = [
        doc["Age"]
        for doc in documents
        if "Age" in doc
        and isinstance(doc["Age"], int)
        and (doc["Age"] < 0 or doc["Age"] > 120)
    ]

    if invalid_ages:
        print(f" {len(invalid_ages)} âge(s) invalide(s)")
        errors = True
    else:
        print(" Tous les âges sont plausibles")

    # ==============================
    # Résultat final
    # ==============================

    print("\n--- Résultat final ---")

    if errors:
        print(" Erreurs critiques détectées. Arrêt du programme.")
        client.close()
        sys.exit(1)
    else:
        print(" Validation réussie. Aucune erreur critique.")
        client.close()
        sys.exit(0)


if __name__ == "__main__":
    main()