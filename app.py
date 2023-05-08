from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from python.helpers import login_required, get_days_in_week
import python.database as database
import python.validate_userinput as validate


# Configure application
app = Flask(__name__)

# setup db an check if users table exists
db = database.SQLite("project.db")
database.create_users(db)

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

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # user reached route via get
    if not request.method == "POST":
        date = get_days_in_week()
        date_value = datetime.date.today()
    

    if request.method == "POST":
        date_value = request.form["date"]
        requested_date = datetime.datetime.strptime(request.form["date"], "%Y-%m-%d")
        date = get_days_in_week(requested_date)

    #get user posts from db
    table = f"posts_{session['user_id']}" 
    user_posts = db.execute(f"SELECT * from {table}")  
    print(user_posts)
    print(date)   
    return render_template("index.html", date=date, date_value=date_value, user_posts=user_posts)

@app.route("/submit", methods=["POST"])
@login_required
def submit(): 
    """ Writes user Post to the database """ 
    valid_input, alert_message = validate.submit(request.form)
    if not valid_input:
        date = get_days_in_week()
        date_value = datetime.date.today()
        return render_template("index.html", date=date, date_value=date_value, alert= alert_message)
    table = f"posts_{session['user_id']}"
    db.execute(f"INSERT INTO {table} (thema, start, end, type, day) VALUES(?, ?, ?, ?, ?)", (request.form["thema"], request.form["start"], request.form["end"], request.form["type"], request.form["day"]))    
    
    return redirect("/")

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
        valid_input, alert_message = validate.login(request.form)
        if not valid_input:
            return render_template("login.html", alert=alert_message)

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

       valid_input, alert_message = validate.register(request.form)
       if not valid_input:
            return render_template("register.html", alert=alert_message)
       
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