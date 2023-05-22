from functools import wraps
from flask import session, redirect
import datetime


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

def get_days_in_week(date=None):
    if date == None:
        date = datetime.date.today()
    days_in_week = {
        "year": date.year,
        "month": [],
        "day": [],
        "week_days": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
        "date": []
    }
    # Get the day of the week (Monday = 0, Sunday = 6)
    weekday = date.weekday()
        # Calculate the start and end dates of the week
    start_date = date - datetime.timedelta(weekday)
    end_date = start_date + datetime.timedelta(6)
        # Generate a list of all the days in the week
    current_date = start_date

    while current_date <= end_date:
        days_in_week["day"].append(current_date.day)
        days_in_week["month"].append(current_date.month)
        days_in_week["date"].append(current_date.strftime("%Y-%m-%d"))
        current_date += datetime.timedelta(days=1)
    
    return(days_in_week)