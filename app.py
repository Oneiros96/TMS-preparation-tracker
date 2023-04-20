from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from python.helpers import login_required, SQLite
import python.database as database

# Configure application
app = Flask(__name__)

# setup db
db = SQLite("project.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def todo():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """
    # Forget any user_id
    session.clear()
    
    # User reached route via GET
    if not request.method == "POST":
        return render_template("login.html")
    # User trys to log in
    if request.method == "POST":
        if not request.form["username"]:
            return render_template("login.html", alert="Bite gib einen Username ein.")
        if not request.form["password"]:
            return render_template("login.html", alert="Bitte gib ein Passwort ein.")
    
    user = db.execute("SELECT * FROM users WHERE username = ?", (request.form["username"],))
    
    if len(user) != 1 or not check_password_hash(user[0]["password_hash"], request.form["password"]):
        return render_template("login.html", alert="Falscher Username oder Passwort.")
    
    session["user_id"] = user[0]["user_id"]
    
    
    return redirect("/")

@app.route("/register", methods=["GET", "POST"]) 
def register():
    """ Enable users to register """
    # Forget any user_id
    session.clear()

    # User reached route via GET
    if not request.method == "POST":
        return render_template("register.html")
    
    if request.method == "POST":

        ### Form validation ###

        # Username provided and available        
        if not request.form["username"]:
            return render_template("register.html", alert="Bitte wähle einen Username.")
        
        if db.execute("SELECT username FROM users WHERE username = ?", (request.form["username"],)):            
            return render_template("register.html", alert="Username nicht verfügbar.")
        
        # Password provided and match confirmation
        if not request.form["password"]:
            return render_template("register.html", alert="Bitte wähle ein Passwort.")
        if not request.form["password"] == request.form["confirmation"]:
            return render_template("register.html", alert="Passwort und Bestätigung müssen überein stimmen.")

        # generate password hash and write user to db
        hash = generate_password_hash(request.form["password"])
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (request.form["username"], hash))
        
        # log user in
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", (request.form["username"],))
        
        session["user_id"] = user_id[0]["user_id"]
        database.create_user_comments(user_id[0]["user_id"], db)
        database.create_user_posts(user_id[0]["user_id"], db)
        return redirect("/")
        
@app.route("/logout")     
def logout():
    session.clear()
    return redirect("/")