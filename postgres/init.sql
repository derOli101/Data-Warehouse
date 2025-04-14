-- Schema "inventory" anlegen – wird zur logischen Gruppierung der Tabelle verwendet
CREATE SCHEMA inventory;

-- Tabelle "customers" im Schema "inventory" anlegen
CREATE TABLE inventory.customers (
    id SERIAL PRIMARY KEY,       -- Automatisch inkrementierender Primärschlüssel
    first_name VARCHAR(255),     -- Vorname des Kunden
    last_name VARCHAR(255),      -- Nachname des Kunden
    email VARCHAR(255)           -- E-Mail-Adresse des Kunden
);

-- Publication für logical replication einrichten
-- Debezium benötigt diese, um Änderungen an der Tabelle zu erkennen
CREATE PUBLICATION debezium_pub FOR TABLE inventory.customers;

-- Hinweis: Der Replikations-Slot wird **nicht** hier erstellt,
-- sondern später automatisch von Debezium beim ersten Start erzeugt

-- Berechtigung sicherstellen: Benutzer "postgres" bekommt Superuser-Rechte
-- (Kann in Docker-Umgebungen nötig sein, wenn der Benutzer standardmäßig eingeschränkt ist)
ALTER USER postgres WITH SUPERUSER;
