print("Création des utilisateurs et rôles");

// Sélection de la base

db = db.getSiblingDB("healtcare");

// 1. Administrateur de la base
db.createUser({
    user: "healtcare",
    pwd: "healtcare",
    roles: [
        { role: "readWrite", db: "healtcare" },
        { role: "dbAdmin", db: "healtcare" },
        { role: "userAdmin", db: "healtcare" }
    ]
});

// 2. Application métier
db.createUser({
    user: "technicien",
    pwd: "Technicienhealtare",
    roles: [
        { role: "readWrite", db: "healtcare" }
    ]
});

//3. Lecture seule
db.createUser({
    user: "client",
    pwd: "Clienthealtcare",
    roles: [
        { role: "read", db: "healtcare" }
    ]
});

print("Tous les 3 utilisateurs ont été créés avec succès !");