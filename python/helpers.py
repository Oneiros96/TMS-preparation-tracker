from functools import wraps
from flask import session, redirect
import calendar
import datetime
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

def today():
    today = datetime.date.today()
    formated_month = "{:02d}".format(today.month)
    date = {
        "year": today.year,
        "month":formated_month,
        "day": today.day,
        "week_days": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    }
    date["week"] = get_week(date)
    return(date)

def get_week(date):    


    obj = calendar.monthcalendar(date["year"], int(date["month"]))

    for week in obj:
        for day in week:
            if date["day"] == day:
                return (week)


