
import sqlite3



def create_users(db):
    """ creates users table"""

    db.execute(
        "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password_hash TEXT NOT NULL, registered_at DATETIME NOT NULL DEFAULT (datetime('now')))"
        )  
    

def create_user_posts(user_id, db):
    """ create user specific posts table """

    query = f"CREATE TABLE posts_{user_id} (post_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, thema TEXT NOT NULL, start TIME NOT NULL, end TIME NOT NULL, type TEXT NOT NULL, day DATE NOT NULL)"
    db.execute(query)

def create_user_comments(user_id, db):
    """ create user specific comments table """
    query = f"CREATE TABLE comments_{user_id} (comment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, post_id INTEGER UNIQUE NOT NULL, points_possible INTEGER, points_reached INTEGER, noticeable TEXT DEFAULT '', to_improve TEXT DEFAULT '', strategys TEXT DEFAULT '')"
    db.execute(query)

class SQLite:
    """ Setup connection to database when needed and close it after querry"""
    #  Init and specify db-file
    def __init__(self, database_file):
        self.database_file = database_file
        self.connection = None


    def connect(self):
        self.connection = sqlite3.connect(self.database_file)
        # print executed query's to console
        self.connection.set_trace_callback(print)
    

    
    def close(self):
        if self.connection:
            self.connection.close()

    def execute(self, query, params=None):
        # create connection and cursor
        self.connect()
        cursor = self.connection.cursor()
        # To make the output a list of dict's, with the Column names as keys
        cursor.row_factory = sqlite3.Row
        # Check if querry is an prepared statement and execute
        if params:
            cursor.execute(query, params)
            
        else:
            cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        # commit and close
        self.connection.commit()
        self.close()
        return results