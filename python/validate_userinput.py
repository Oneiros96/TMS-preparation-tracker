import os
import python.database as database
import datetime


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

def submit_post(userinput):
    themas = ("Muster zuordnen",
              "Quantitative und formlae Probleme",
              "Schlauchfiguren",
              "Med./Naturw. Grundverständnis",
              "Figuren lernen",
              "Fakten lernen",
              "Textverständnis",
              "Diagramme und Tablellen")
    types = ("Übung",
             "Theorie",
             "Simulation",
             "Video/Meeting",
             "Bootcamp")

    
        
    if not userinput["start"]:
        return False, "Bitte wähle eine Startzeit."
    if not userinput["end"]:
        return False, "Bitte wähle ein ende."
    if not userinput["day"]:
        return False, "Bitte wähle ein Datum."
    if not themas.count(userinput["thema"]):
        return False, "Bitte wähle ein Thema."
    if not types.count(userinput["type"]):
         return False, "Bitte wähle die Art der übung."
    else:
        return True, ""
         