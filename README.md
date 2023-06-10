# TMS - preparation tracker

### *currently it's required to use 24h time format and dd/mm/yyyy settings in the browser for corract funktionally. Will be fixed* ###

Welcome to the TMS - preparation tracker repository!
This webapp created with python and Flask aims to provide an easy solution to track learning sessions and make comments for each of them, 
while preparing for the german TMS(Test für Medizinische Studiengänge).
This app can be used by individual Students or by course providers to supply their customers with it. 
**Please mind while code and comments are written in english, as this is an app for future german medizin students, the content of the redered websites is in german.**

## Features

- User registration and authentification
- Weekly overview to which you can add and delete diffrent kind's of learning sessions(Übung, Theorie, Simulation, Video/Meeting, Bootcamp) for the 8 theoretically of the test
- adding and deleting comments to each posted leraning session

## Usage
1. Register/Login: Create a new account or log in using your existing credentials.
2. Übersicht: Upon logging you will be redirected to the Übersicht page, where you are provided with a weekly dashboard to which you can add your learning session
3. Kommentare: Here you can add comments to evry kearning session posted on Übersicht
4. Logout: End your current session an return to the login page
### Video Demo: https://youtu.be/NMI1HUBIP3Q

## Used technology

- python 3.11
- Flask 2.2.3
- Flask-Session 0.4.0
- html
- CSS /  Bootstrap 5.1
- JS
- jinja 2

## Files
/app.py Contains the main logic for the backend. Which includes to call funktions for database connection and if runned the first time setup, session setup and the callable routes

/python/databse.py contains the SQLite class for seting up db connections, execute querys's and close the connection. As well as console logging executed query's. Additionaly it contains funktions for initial db creation and to add user specific post and comments tables

/python/helpers.py Currently containing the functions for the @login_required decorator and the get_days_in_week funtion which provides the object used to render the head of the dashboard on index.html.

/python/validate_userinput.py Collection of funcions to validate user input. All functions are designed to take userinput and if needed additional arguments as input and return False and an alert message, if the validation fails or return true if they pass.

/static/styles.css basic css customization

/templates/layout.html basic website layout extended by the following .html files
/templates/login.html login page
/templates/register.html registration page
/templates/index.html main page containing the weekly dashboard for tracking learning sessions
/templates/comments.html comments page

/requirements.txt  created with pip freeze to easily recreated the venv used in production

## License
The TMS Preparation Tracker is licensed under the [MIT License](https://github.com/Oneiros96/TMS-preparation-tracker/blob/main/LICENSE). Feel free to use, modify, and distribute the software as permitted by the license.
