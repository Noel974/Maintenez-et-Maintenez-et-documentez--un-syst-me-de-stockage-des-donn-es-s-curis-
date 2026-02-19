import os
from pymongo import MongoClient
from dotenv import load_dotenv
from collections import Counter

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

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION]

    print("📥 Lecture des données depuis MongoDB...")
    documents = list(collection.find({}, {"_id": 0}))  # on ignore _id

    if not documents:
        print("⚠️ Aucune donnée trouvée.")
        return

    print(f"📊 Nombre de documents : {len(documents)}")

    # ==============================
    # 1️⃣ Vérification des colonnes
    # ==============================

    print("\n--- Vérification des colonnes ---")

    all_keys = set()
    for doc in documents:
        all_keys.update(doc.keys())

    missing = set(EXPECTED_FIELDS.keys()) - all_keys
    extra = all_keys - set(EXPECTED_FIELDS.keys())

    if not missing:
        print("✅ Toutes les colonnes sont présentes")
    else:
        print("❌ Colonnes manquantes :", missing)

    if extra:
        print("⚠️ Colonnes supplémentaires :", extra)

    # ==============================
    # 2️⃣ Vérification des types
    # ==============================

    print("\n--- Vérification des types ---")

    for field, expected_type in EXPECTED_FIELDS.items():
        for doc in documents:
            if field in doc and doc[field] is not None:
                if not isinstance(doc[field], expected_type):
                    print(f"⚠️ Mauvais type pour {field} : {type(doc[field])} (attendu : {expected_type})")
                    break
        else:
            print(f"✅ Type correct pour {field}")

    # ==============================
    # 3️⃣ Valeurs manquantes
    # ==============================

    print("\n--- Vérification des valeurs manquantes ---")

    for field in EXPECTED_FIELDS.keys():
        missing_count = sum(1 for doc in documents if field not in doc or doc[field] is None)
        if missing_count > 0:
            print(f"❌ {missing_count} valeur(s) manquante(s) dans {field}")
        else:
            print(f"✅ Pas de valeur manquante dans {field}")

    # ==============================
    # 4️⃣ Doublons
    # ==============================

    print("\n--- Vérification des doublons ---")

    # On considère qu'une ligne entière identique = doublon
    doc_tuples = [tuple(sorted(doc.items())) for doc in documents]
    duplicates = len(doc_tuples) - len(set(doc_tuples))

    if duplicates > 0:
        print(f"❌ {duplicates} doublon(s) détecté(s)")
    else:
        print("✅ Aucun doublon détecté")

    # ==============================
    # 5️⃣ Validité des âges
    # ==============================

    print("\n--- Vérification des âges ---")

    invalid_ages = [
        doc["Age"]
        for doc in documents
        if "Age" in doc and isinstance(doc["Age"], int)
        and (doc["Age"] < 0 or doc["Age"] > 120)
    ]

    if invalid_ages:
        print(f"❌ {len(invalid_ages)} âge(s) invalide(s)")
    else:
        print("✅ Tous les âges sont plausibles")

    print("\n✅ Test d’intégrité après migration terminé.")
    client.close()


if __name__ == "__main__":
    main()
