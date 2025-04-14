import redis
import json

# Verbindung zum Redis-Server herstellen
# Falls Redis in einem Container läuft und von außen erreichbar ist, ggf. "localhost" durch "host.docker.internal" ersetzen
r = redis.Redis(host='localhost', port=6379)

# Name des Redis-Streams, in dem Debezium die Change Events publiziert
stream = "tutorial.inventory.customers"

# Alle Events aus dem Stream abrufen (XRANGE: alle Einträge von Anfang bis Ende)
entries = r.xrange(stream)

# Iteration über alle Events im Stream
for entry_id, fields in entries:
    print(f"\n Event-ID: {entry_id.decode()}")  # Anzeige der Event-ID (Zeitbasiert, Redis-Stream ID)

    # Jedes Event enthält ein Key-Value-Paar (meist: "key" und "value")
    for key, raw_val in fields.items():
        key_str = key.decode()       # Redis liefert Bytes → in Strings umwandeln
        val_str = raw_val.decode()   # Auch der Wert wird als String interpretiert

        try:
            # Falls Inhalt JSON ist: schön formatiert ausgeben
            val = json.loads(val_str)
            print(f" {key_str}:")
            print(json.dumps(val, indent=4))  # JSON mit Einrückung anzeigen
        except json.JSONDecodeError:
            # Falls kein valides JSON (z. B. bei Debug-Ausgaben o. ä.)
            print(f" {key_str}: {val_str} (kein JSON)")
