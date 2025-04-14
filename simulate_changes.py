import psycopg2
import time

# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
    host="127.0.0.1",         # Lokale Verbindung (Docker-Port muss an Host gebunden sein)
    port="5432",              # Standard-Port für PostgreSQL
    user="postgres",          # Benutzername
    password="postgres",      # Passwort
    dbname="postgres"         # Datenbankname
)

cursor = conn.cursor()

# Sicherstellen, dass Schema und Tabelle existieren (idempotent)
cursor.execute("""
CREATE SCHEMA IF NOT EXISTS inventory;

CREATE TABLE IF NOT EXISTS inventory.customers (
    id SERIAL PRIMARY KEY,               -- Automatisch generierter Primärschlüssel
    first_name VARCHAR(255),             -- Vorname
    last_name VARCHAR(255),              -- Nachname
    email VARCHAR(255)                   -- E-Mail-Adresse
);
""")
conn.commit()

# INSERT: Einen neuen Datensatz hinzufügen
print("▶️ Füge neuen Kunden ein...")
cursor.execute("""
INSERT INTO inventory.customers (first_name, last_name, email)
VALUES (%s, %s, %s);
""", ('Erika', 'Mustermann', 'erika@example.com'))
conn.commit()

time.sleep(2)  # Kleine Verzögerung zur besseren Erkennbarkeit im Debezium-Log

# UPDATE: E-Mail-Adresse des Kunden ändern
print("🔄 Aktualisiere Kunden-E-Mail...")
cursor.execute("""
UPDATE inventory.customers
SET email = %s
WHERE first_name = %s AND last_name = %s;
""", ('erika.m@example.com', 'Erika', 'Mustermann'))
conn.commit()

time.sleep(2)  # Wieder kurze Verzögerung

# DELETE: Kundendatensatz löschen
print("🗑 Lösche Kunden...")
cursor.execute("""
DELETE FROM inventory.customers
WHERE first_name = %s AND last_name = %s;
""", ('Erika', 'Mustermann'))
conn.commit()

print("✅ Fertig.")

# Ressourcen freigeben
cursor.close()
conn.close()
