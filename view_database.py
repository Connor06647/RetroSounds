import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Query all users
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

# Display the results
print("Database Contents:")
print("=" * 50)
print(f"{'ID':<5} | {'Name':<20} | {'Email':<30}")
print("-" * 50)

if rows:
    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<30}")
else:
    print("No data found in database")

print(f"\nTotal records: {len(rows)}")

conn.close()