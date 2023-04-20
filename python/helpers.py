from functools import wraps
from flask import session, redirect
import sqlite3
import logging

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

class SQLite:
    """ Setup connection to database when needed and close it after querry"""
    #  Init and specify db-file
    def __init__(self, database_file):
        self.database_file = database_file
        self.connection = None


    def connect(self):
        self.connection = sqlite3.connect(self.database_file)
        # TODO implement log instead of print
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

