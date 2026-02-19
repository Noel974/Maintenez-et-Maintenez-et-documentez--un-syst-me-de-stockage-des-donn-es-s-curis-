import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")

if not CSV_FILE:
    print("❌ Variable CSV_FILE non définie dans le .env")
    sys.exit(1)

def generate_expected_columns(csv_file):
    df = pd.read_csv(csv_file)

    expected_columns = {}

    for col in df.columns:
        expected_columns[col] = str(df[col].dtype)

    return expected_columns


if __name__ == "__main__":
    expected = generate_expected_columns(CSV_FILE)

    print("EXPECTED_COLUMNS = {")
    for key, value in expected.items():
        print(f'    "{key}": "{value}",')
    print("}")
