import redis
import time

# Verbindung zu Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


# Felder
status = True
expireTime = 3600  # 1 Stunde


# Funktionen
#
# Funktion zur Erstellung eines Profils
def erstelle_profil():
    email = input("E-Mail-Adresse: ")
    email = email.lower()
    # Überprüfen, ob das Profil bereits vorhanden ist
    if r.exists(email):
        print("Ein Profil mit dieser E-Mail-Adresse existiert bereits")
        return
    passwort = input("Passwort: ")
    name = input("Name: ")
    adresse = input("Adresse: ")

    # Profil erstellen und in Redis speichern
    r.hset(email, "email", email)
    r.hset(email, "passwort", passwort)
    r.hset(email, "name", name)
    r.hset(email, "adresse", adresse)

    # Login-Zeit hinzufügen
    add_login_zeit(email)

    # Expiration hinzufügen
    r.expire(email, expireTime)


# Funktion zum Abrufen eines Profils
def hole_profil():
    email = input("E-Mail-Adresse: ")
    email = email.lower()
    # Überprüfen, ob das Profil vorhanden ist
    if not r.exists(email):
        print("Ein Profil mit dieser E-Mail-Adresse existiert nicht")
        return

    # Profil abrufen und zurückgeben
    print(r.hgetall(email))
    login_zeiten = r.lrange(email + ":login_zeiten", 0, -1)
    print("Login-Zeiten:")
    for login_zeit in login_zeiten:
        print(login_zeit)

# Funktion zum Hinzufügen einer Login-Zeit
def add_login_zeit(email=None):
    if email is None:
        email = input("E-Mail-Adresse: ")
        email = email.lower()
    # Überprüfen, ob das Profil vorhanden ist
    if not r.exists(email):
        print("Ein Profil mit dieser E-Mail-Adresse existiert nicht")
        return

    # Aktuelle Zeit hinzufügen
    login_zeit = time.strftime("%Y-%m-%d %H:%M:%S")
    r.lpush(email + ":login_zeiten", login_zeit)

    # Expiration erneuern
    r.expire(email, expireTime)

# Funktion zum Löschen eines Profils
def loesche_profil():
    email = input("E-Mail-Adresse: ")
    email = email.lower()
    # Überprüfen, ob das Profil vorhanden ist
    if not r.exists(email):
        print("Ein Profil mit dieser E-Mail-Adresse existiert nicht")
        return

    # Profil löschen
    r.delete(email)
    print(f"Das Profil mit der E-Mail-Adresse {email} wurde gelöscht.")

# Funktion zum Anzeigen aller Profile
def zeige_alle_profile():
    # Alle Schlüssel der Profiele in Redis abrufen
    keys = r.keys()

    if not keys:
        print("Es sind keine Profile vorhanden")
        return
    #Zählen wie viele Profile vorhanden sind
    print(f"Es sind {len(keys)/2} Profile vorhanden")
    #Alle Profile anzeigen
    print("Alle Profile:")
    for key in keys:
        # Nur Profile anzeigen
        if r.type(key) == "hash":
            print("")
            print(r.hgetall(key))
            login_zeiten = r.lrange(key + ":login_zeiten", 0, -1)
            print("Login-Zeiten:")
            for login_zeit in login_zeiten:
                print(login_zeit)

# Funktion zum Löschen aller Profile
def alle_loeschen():
    r.flushall()
    print("Alle Profile wurden gelöscht.")


# Programm Loop
while status:
    print("")
    print("Navigation")
    print("1. User hinzufügen")
    print("2. User anzeigen")
    print("3. Login-Zeit hinzufügen")
    print("4. Profiel löschen")
    print("5. Alle Profile anzeigen")
    print("6. Alle Prfiele löschen")
    print("7. Exit")
    user_input = input("Navigation Number: ")
    if user_input == "1":
        erstelle_profil()
    elif user_input == "2":
        hole_profil()
    elif user_input == "3":
        add_login_zeit()
    elif user_input == "4":
        loesche_profil()
    elif user_input == "5":
        zeige_alle_profile()
    elif user_input == "6":
        alle_loeschen()
    elif user_input == "7":
        status = False
    else:
        print("Invalid Input")
