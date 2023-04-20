
from python.helpers import SQLite
import os


#def create_users():
 #   """ creates users table"""

  #  db.execute(
   #     "CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password_hash TEXT NOT NULL, registered_at DATETIME NOT NULL DEFAULT (datetime('now')))"
    #    )  
    

def create_user_posts(user_id, db):
    """ create user specific posts table """
    query = f"CREATE TABLE posts_{user_id} (post_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, thema TEXT NOT NULL, start TIME NOT NULL, end TIME NOT NULL, type TEXT NOT NULL, day DATE NOT NULL)"
    db.execute(query)
    print(query)
    

    
def create_user_comments(user_id, db):
    query = f"CREATE TABLE comments_{user_id} (comment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, theme TEXT NOT NULL, post_id INTEGER UNIQUE NOT NULL, points_possible INTEGER, points_reached INTEGER, noticeable TEXT DEFAULT '', to_improve TEXT DEFAULT '', strategys TEXT DEFAULT '')"
    print(query)
    db.execute(query)

