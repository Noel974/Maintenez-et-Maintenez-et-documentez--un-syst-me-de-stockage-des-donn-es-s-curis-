import os
import sys
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# ==========================
#  CHARGEMENT CONFIGURATION (.env)
# ==========================

load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")

required_vars = {
    "CSV_FILE": CSV_FILE,
    "MONGO_DB_NAME": MONGO_DB_NAME,
    "MONGO_COLLECTION": MONGO_COLLECTION,
    "MONGO_URI": MONGO_URI
}

for var_name, value in required_vars.items():
    if not value:
        print(f" Variable {var_name} non définie dans le .env")
        sys.exit(1)

if not os.path.exists(CSV_FILE):
    print(f" Le fichier {CSV_FILE} n'existe pas.")
    sys.exit(1)

print(" Configuration chargée avec succès")

# ==========================
#  CHARGEMENT DONNÉES
# ==========================

def load_csv(csv_file):
    return pd.read_csv(csv_file)


def load_mongodb(uri, db_name, collection_name):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        data = list(collection.find({}, {"_id": 0}))
        client.close()
        return pd.DataFrame(data)
    except Exception as e:
        print(" Erreur connexion MongoDB :", e)
        sys.exit(1)

# ==========================
#  COMPARAISON
# ==========================

def compare_data(csv_df, mongo_df):

    print("\n=== COMPARAISON CSV vs MONGODB ===")

    error = False

    # Harmonisation
    csv_df = csv_df.fillna("NA")
    mongo_df = mongo_df.fillna("NA")

    print("\nNombre de lignes :")
    print("CSV :", len(csv_df))
    print("MongoDB :", len(mongo_df))

    if len(csv_df) != len(mongo_df):
        print("Nombre de lignes différent")
        error = True
    else:
        print("Même nombre de lignes")

    # Vérification colonnes
    if set(csv_df.columns) != set(mongo_df.columns):
        print("Colonnes différentes")
        print("CSV uniquement :", set(csv_df.columns) - set(mongo_df.columns))
        print("Mongo uniquement :", set(mongo_df.columns) - set(csv_df.columns))
        error = True
        
        # ⚠️ AVERTISSEMENT :
        # Un sys.exit() est déclenché ici.
        # Tout le code situé après cet appel dans la fonction
        # ne sera jamais exécuté.
        sys.exit(1)

    else:
        print("Colonnes identiques")

    # Trier pour comparaison
    csv_sorted = csv_df.sort_values(by=list(csv_df.columns)).reset_index(drop=True)
    mongo_sorted = mongo_df.sort_values(by=list(mongo_df.columns)).reset_index(drop=True)

    if csv_sorted.equals(mongo_sorted):
        print("\nLes données sont STRICTEMENT identiques")
        print("\n--- Résultat final ---")
        print("Migration validée : données parfaitement identiques")
        sys.exit(0)

    print("\nLes données sont différentes")
    error = True

    # =====================================================
    #  DIAGNOSTIC DÉTAILLÉ
    # =====================================================

    print("\n--- Analyse détaillée des différences ---")

    # ⚠️ AVERTISSEMENT :
    # diff_csv est calculé mais jamais utilisé ensuite.
    diff_csv = pd.concat([csv_sorted, mongo_sorted]).drop_duplicates(keep=False)

    # ⚠️ AVERTISSEMENT :
    # Double appel à pd.merge avec logique similaire.
    only_in_csv = pd.merge(csv_sorted, mongo_sorted, how='outer', indicator=True)
    only_in_csv = only_in_csv[only_in_csv['_merge'] == 'left_only']

    only_in_mongo = pd.merge(csv_sorted, mongo_sorted, how='outer', indicator=True)
    only_in_mongo = only_in_mongo[only_in_mongo['_merge'] == 'right_only']

    if not only_in_csv.empty:
        print(f"\n{len(only_in_csv)} ligne(s) présente(s) dans CSV mais absente(s) dans MongoDB")
        print(only_in_csv.head(3))

    if not only_in_mongo.empty:
        print(f"\n{len(only_in_mongo)} ligne(s) présente(s) dans MongoDB mais absente(s) dans CSV")
        print(only_in_mongo.head(3))

    # Comparaison cellule par cellule si tailles identiques
    if len(csv_sorted) == len(mongo_sorted):
        diff_cells = (csv_sorted != mongo_sorted)
        total_differences = diff_cells.sum().sum()

        if total_differences > 0:
            print(f"\n{total_differences} cellule(s) différente(s) détectée(s)")

            rows, cols = diff_cells.to_numpy().nonzero()
            print("\nExemples de différences :")
            for i in range(min(5, len(rows))):
                r = rows[i]
                c = cols[i]
                col_name = csv_sorted.columns[c]
                print(
                    f"Ligne {r}, Colonne '{col_name}' : "
                    f"CSV={csv_sorted.iloc[r, c]} | "
                    f"MongoDB={mongo_sorted.iloc[r, c]}"
                )

    print("\n--- Résultat final ---")
    print("Différences détectées entre CSV et MongoDB")

    # ⚠️ AVERTISSEMENT :
    # Tout le bloc de code dupliqué situé après ce sys.exit()
    # dans la version originale ne sera jamais exécuté.
    sys.exit(1)
    print("\n=== COMPARAISON CSV vs MONGODB ===")

    error = False

    # Harmonisation
    csv_df = csv_df.fillna("NA")
    mongo_df = mongo_df.fillna("NA")

    print("\nNombre de lignes :")
    print("CSV :", len(csv_df))
    print("MongoDB :", len(mongo_df))

    if len(csv_df) != len(mongo_df):
        print(" Nombre de lignes différent")
        error = True
    else:
        print(" Même nombre de lignes")

    # Vérification colonnes
    if set(csv_df.columns) != set(mongo_df.columns):
        print(" Colonnes différentes")
        print("CSV uniquement :", set(csv_df.columns) - set(mongo_df.columns))
        print("Mongo uniquement :", set(mongo_df.columns) - set(csv_df.columns))
        error = True
        return sys.exit(1)
    else:
        print(" Colonnes identiques")

    # Trier pour comparaison
    csv_sorted = csv_df.sort_values(by=list(csv_df.columns)).reset_index(drop=True)
    mongo_sorted = mongo_df.sort_values(by=list(mongo_df.columns)).reset_index(drop=True)

    if csv_sorted.equals(mongo_sorted):
        print("\n Les données sont STRICTEMENT identiques")
        print("\n--- Résultat final ---")
        print(" Migration validée : données parfaitement identiques")
        sys.exit(0)

    print("\n Les données sont différentes")
    error = True

    # =====================================================
    #  DIAGNOSTIC DÉTAILLÉ
    # =====================================================

    print("\n--- Analyse détaillée des différences ---")

    # Lignes présentes dans CSV mais absentes dans MongoDB
    diff_csv = pd.concat([csv_sorted, mongo_sorted]).drop_duplicates(keep=False)
    only_in_csv = pd.merge(csv_sorted, mongo_sorted, how='outer', indicator=True)
    only_in_csv = only_in_csv[only_in_csv['_merge'] == 'left_only']
    only_in_mongo = pd.merge(csv_sorted, mongo_sorted, how='outer', indicator=True)
    only_in_mongo = only_in_mongo[only_in_mongo['_merge'] == 'right_only']

    if not only_in_csv.empty:
        print(f"\n {len(only_in_csv)} ligne(s) présente(s) dans CSV mais absente(s) dans MongoDB")
        print(only_in_csv.head(3))  # affiche 3 exemples

    if not only_in_mongo.empty:
        print(f"\n {len(only_in_mongo)} ligne(s) présente(s) dans MongoDB mais absente(s) dans CSV")
        print(only_in_mongo.head(3))  # affiche 3 exemples

    # Comparaison cellule par cellule si tailles identiques
    if len(csv_sorted) == len(mongo_sorted):
        diff_cells = (csv_sorted != mongo_sorted)
        total_differences = diff_cells.sum().sum()

        if total_differences > 0:
            print(f"\n {total_differences} cellule(s) différente(s) détectée(s)")
            
            rows, cols = diff_cells.to_numpy().nonzero()
            print("\nExemples de différences :")
            for i in range(min(5, len(rows))):
                r = rows[i]
                c = cols[i]
                col_name = csv_sorted.columns[c]
                print(f"Ligne {r}, Colonne '{col_name}' : CSV={csv_sorted.iloc[r, c]} | MongoDB={mongo_sorted.iloc[r, c]}")

    print("\n--- Résultat final ---")
    print(" Différences détectées entre CSV et MongoDB")
    sys.exit(1)
    print("\n=== COMPARAISON CSV vs MONGODB ===")

    error = False

    # Harmoniser valeurs manquantes
    csv_df = csv_df.fillna("NA")
    mongo_df = mongo_df.fillna("NA")

    # ==========================
    # Nombre de lignes
    # ==========================

    print("\nNombre de lignes :")
    print("CSV :", len(csv_df))
    print("MongoDB :", len(mongo_df))

    if len(csv_df) == len(mongo_df):
        print(" Même nombre de lignes")
    else:
        print(" Nombre de lignes différent")
        error = True

    # ==========================
    # Colonnes
    # ==========================

    if set(csv_df.columns) == set(mongo_df.columns):
        print(" Colonnes identiques")
    else:
        print(" Colonnes différentes")
        print("CSV :", set(csv_df.columns))
        print("MongoDB :", set(mongo_df.columns))
        error = True

    # ==========================
    # Comparaison complète
    # ==========================

    try:
        csv_sorted = csv_df.sort_values(by=list(csv_df.columns)).reset_index(drop=True)
        mongo_sorted = mongo_df.sort_values(by=list(mongo_df.columns)).reset_index(drop=True)

        if csv_sorted.equals(mongo_sorted):
            print("\n Les données sont STRICTEMENT identiques")
        else:
            print("\n Les données sont différentes")
            error = True

    except Exception as e:
        print(" Erreur lors de la comparaison :", e)
        error = True

    # ==========================
    # Résultat final
    # ==========================

    print("\n--- Résultat final ---")

    if error:
        print(" Différences détectées entre CSV et MongoDB")
        sys.exit(1)
    else:
        print(" Migration validée : données parfaitement identiques")
        sys.exit(0)


# ==========================
#  MAIN
# ==========================

if __name__ == "__main__":

    csv_df = load_csv(CSV_FILE)
    mongo_df = load_mongodb(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION)

    compare_data(csv_df, mongo_df)