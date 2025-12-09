from flask import Flask, request, send_from_directory, jsonify
import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime
import csv
import io

DB = 'users.db'
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DB)
    # Create users table with timestamp
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Add created_at column to existing table if it doesn't exist
    try:
        conn.execute('ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    except sqlite3.OperationalError:
        pass  # Column already exists
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

@app.route('/themes')
def themes():
    # serve the theme browser
    return send_from_directory('.', 'theme-browser.html')

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

@app.route('/admin')
def admin():
    # serve the admin dashboard page
    return send_from_directory('.', 'admin.html')

@app.route('/api/users')
def get_users():
    # API endpoint to get all users as JSON with sorting
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'desc')
    
    allowed_columns = ['id', 'name', 'email', 'created_at']
    if sort_by not in allowed_columns:
        sort_by = 'id'
    if order not in ['asc', 'desc']:
        order = 'desc'
    
    conn = get_db()
    query = f'SELECT id, name, email, created_at FROM users ORDER BY {sort_by} {order}'
    cursor = conn.execute(query)
    users = [{'id': row[0], 'name': row[1], 'email': row[2], 'created_at': row[3]} for row in cursor.fetchall()]
    conn.close()
    return {'users': users, 'count': len(users)}

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # API endpoint to delete a user
    conn = get_db()
    try:
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return {'success': True, 'message': 'User deleted'}
    except Exception as e:
        conn.close()
        return {'success': False, 'message': str(e)}, 400

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # API endpoint to update a user
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return {'success': False, 'message': 'Name and email required'}, 400
    
    conn = get_db()
    try:
        conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
        conn.commit()
        conn.close()
        return {'success': True, 'message': 'User updated'}
    except Exception as e:
        conn.close()
        return {'success': False, 'message': str(e)}, 400

@app.route('/api/users/bulk-delete', methods=['POST'])
def bulk_delete_users():
    # API endpoint to delete multiple users
    data = request.json
    user_ids = data.get('ids', [])
    
    if not user_ids:
        return {'success': False, 'message': 'No user IDs provided'}, 400
    
    conn = get_db()
    try:
        placeholders = ','.join('?' * len(user_ids))
        conn.execute(f'DELETE FROM users WHERE id IN ({placeholders})', user_ids)
        conn.commit()
        conn.close()
        return {'success': True, 'message': f'{len(user_ids)} users deleted'}
    except Exception as e:
        conn.close()
        return {'success': False, 'message': str(e)}, 400

@app.route('/api/users/add', methods=['POST'])
def add_user():
    # API endpoint to manually add a user
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return {'success': False, 'message': 'Name and email required'}, 400
    
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return {'success': True, 'message': 'User added successfully'}
    except Exception as e:
        conn.close()
        return {'success': False, 'message': str(e)}, 400

@app.route('/api/users/export')
def export_users():
    # API endpoint to export users as CSV
    conn = get_db()
    cursor = conn.execute('SELECT id, name, email, created_at FROM users ORDER BY id DESC')
    users = cursor.fetchall()
    conn.close()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email', 'Created At'])
    writer.writerows(users)
    
    # Return as downloadable file
    return app.response_class(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=users_export.csv'}
    )

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