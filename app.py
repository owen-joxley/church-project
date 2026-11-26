import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('church.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    # Count total registered members for the live counter display
    member_count = conn.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    # Fetch recent updates or announcements
    conn.close()
    return render_template('index.html', member_count=member_count)

@app.route('/groups')
def groups():
    conn = get_db_connection()
    all_groups = conn.execute("SELECT * FROM groups").fetchall()
    conn.close()
    return render_template('groups.html', groups=all_groups)

@app.route('/sabbath-school')
def sabbath_school():
    # Links out to external SDA Sabbath School lesson portals & quarterly guides
    classes = [
        {"name": "Adult Sabbath School", "external_url": "https://ssnet.org/study-guides/", "desc": "Adult Bible Study Guides & Quarterlies"},
        {"name": "Youth / Real Time Faith", "external_url": "https://www.realtimefaith.net/", "desc": "Sabbath School guide for early teens"},
        {"name": "Cornerstone Connections", "external_url": "https://www.cornerstoneconnections.net/", "desc": "High school youth lessons"},
        {"name": "GraceLink (Children)", "external_url": "https://www.gracelink.net/", "desc": "Beginner, Kindergarten, Primary & PowerPoints"}
    ]
    return render_template('sabbath_school.html', classes=classes)

@app.route('/development')
def development():
    conn = get_db_connection()
    projects = conn.execute("SELECT * FROM development_projects").fetchall()
    conn.close()
    return render_template('development.html', projects=projects)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)