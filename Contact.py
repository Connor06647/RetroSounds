from flask import Flask, request, send_from_directory
import sqlite3
from werkzeug.security import generate_password_hash

DB = 'users.db'
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(DB)

@app.route('/')
def index():
    # serve the home page
    return send_from_directory('.', 'index.html')

@app.route('/products')
def products():
    # serve the products page
    return send_from_directory('.', 'products.html')

@app.route('/login')
def login():
    # serve the login page (your existing Contact.html)
    return send_from_directory('.', 'Contact.html')

@app.route('/Contact.css')
def serve_css():
    # serve the Contact.css file
    return send_from_directory('.', 'Contact.css')

@app.route('/<path:filename>')
def serve_images(filename):
    # serve image files (jpg, png, etc.)
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return send_from_directory('.', filename)
    return 'File not found', 404

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Handle JSON data from HTML
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return 'Missing name or email', 400

    conn = get_db()
    try:
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
    except sqlite3.IntegrityError:
        return 'Error saving user', 400
    finally:
        conn.close()

    return 'User saved successfully', 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)