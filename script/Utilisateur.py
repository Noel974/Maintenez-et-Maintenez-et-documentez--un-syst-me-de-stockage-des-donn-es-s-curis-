from pymongo import MongoClient
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# Chargement du fichier .env
load_dotenv()

# Définition des rôles métier
ROLES = {
    "admin": "Accès complet : import, suppression, mise à jour, logs",
    "user": "Accès standard : lecture + mise à jour",
    "reader": "Lecture seule"
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UtilisateurService:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB_NAME")

        if not mongo_uri or not mongo_db:
            raise ValueError("Variables d'environnement MONGO_URI ou MONGO_DB_NAME manquantes.")

        self.client = MongoClient(mongo_uri)
        self.db = self.client[mongo_db]
        self.users = self.db["users"]

    def creer_utilisateur(self, email, mot_de_passe, roles):
        # Vérifie que les rôles existent
        for role in roles:
            if role not in ROLES:
                raise ValueError(f"Rôle inconnu : {role}")

        # Vérifie si l'utilisateur existe déjà
        if self.users.find_one({"email": email}):
            raise ValueError("Cet utilisateur existe déjà.")

        # Hash du mot de passe
        hash_pwd = pwd_context.hash(mot_de_passe)

        # Insertion dans MongoDB
        self.users.insert_one({
            "email": email,
            "password_hash": hash_pwd,
            "roles": roles
        })

    def verifier_utilisateur(self, email, mot_de_passe):
        user = self.users.find_one({"email": email})
        if not user:
            return False
        return pwd_context.verify(mot_de_passe, user["password_hash"])

    def a_role(self, email, role):
        user = self.users.find_one({"email": email})
        return user and role in user["roles"]
