from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

USER_FILE = 'users.json'
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            # Redirect to the congratulations page after successful login
            return redirect(url_for('congratulations'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists!"
        users[username] = password
        save_users(users)
        return redirect(url_for('login'))
    return render_template('signup.html')

# New route for the congratulations page
@app.route('/congratulations')
def congratulations():
    return render_template('congratulations.html')

app.run(host='0.0.0.0', port=3000)
