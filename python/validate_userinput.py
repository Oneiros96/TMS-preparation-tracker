import os
import python.database as database


def login(userinput):
    if not userinput["username"]:
        return False, "Bite gib einen Username ein."
    if not userinput["password"]:
        return False, "Bitte gib ein Passwort ein."
    else:
        return True, ""

def register(userinput):

    if not userinput["username"]:
        return False, "Bitte wähle einen Username."    
    if not userinput["password"]:
            return False, "Bitte wähle ein Passwort."
    if not userinput["password"] == userinput["confirmation"]:
            return False, "Passwort und Bestätigung müssen überein stimmen."
    
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "project.db")
    print
    db = database.SQLite(db_path)
    if db.execute("SELECT username FROM users WHERE username = ?", (userinput["username"],)):            
            return False, "Username nicht verfügbar."
    else:
        return True, ""
