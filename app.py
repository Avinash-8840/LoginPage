# app.py
from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash  

from pymongo.server_api import ServerApi

uri = "mongodb+srv://avinashsaini8840:bqLs6hqDAR0FQQZK@cluster0.qro4ohl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random string
db = client['dbsparta']
users_collection = db['users']

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index_logged_in.html', username=session['username'])
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = users_collection.find_one({'username': username})

    if user and (user['password'] == password):
        session['username'] = username
        return redirect(url_for('index'))
    return 'Invalid username or password'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
