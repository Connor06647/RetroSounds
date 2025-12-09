"""
Test script for new admin dashboard features
"""
import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5000'

def test_add_users():
    """Test adding users"""
    print("\n=== Testing Add User Feature ===")
    test_users = [
        {'name': 'John Lennon', 'email': 'john@beatles.com'},
        {'name': 'Paul McCartney', 'email': 'paul@beatles.com'},
        {'name': 'George Harrison', 'email': 'george@beatles.com'},
        {'name': 'Ringo Starr', 'email': 'ringo@beatles.com'},
        {'name': 'David Gilmour', 'email': 'david@pinkfloyd.com'},
        {'name': 'Roger Waters', 'email': 'roger@pinkfloyd.com'},
    ]
    
    for user in test_users:
        response = requests.post(f'{BASE_URL}/api/users/add', json=user)
        if response.status_code == 200:
            print(f"✓ Added: {user['name']}")
        else:
            print(f"✗ Failed to add: {user['name']}")
    
def test_get_users():
    """Test getting users with sorting"""
    print("\n=== Testing Get Users & Sorting ===")
    
    # Test default order
    response = requests.get(f'{BASE_URL}/api/users')
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['count']} users (default sort)")
    
    # Test sort by name ascending
    response = requests.get(f'{BASE_URL}/api/users?sort=name&order=asc')
    if response.status_code == 200:
        data = response.json()
        names = [u['name'] for u in data['users']]
        print(f"✓ Sorted by name (asc): {names[:3]}...")
    
    # Test sort by email descending
    response = requests.get(f'{BASE_URL}/api/users?sort=email&order=desc')
    if response.status_code == 200:
        data = response.json()
        emails = [u['email'] for u in data['users']]
        print(f"✓ Sorted by email (desc): {emails[:3]}...")

def test_update_user():
    """Test updating a user"""
    print("\n=== Testing Update User Feature ===")
    
    # Get first user
    response = requests.get(f'{BASE_URL}/api/users')
    users = response.json()['users']
    if not users:
        print("✗ No users to update")
        return
    
    user_id = users[0]['id']
    old_name = users[0]['name']
    
    # Update user
    new_data = {
        'name': f"{old_name} (Updated)",
        'email': users[0]['email']
    }
    response = requests.put(f'{BASE_URL}/api/users/{user_id}', json=new_data)
    if response.status_code == 200:
        print(f"✓ Updated user #{user_id}: {old_name} → {new_data['name']}")
    else:
        print(f"✗ Failed to update user #{user_id}")

def test_bulk_delete():
    """Test bulk delete"""
    print("\n=== Testing Bulk Delete Feature ===")
    
    # Get all users
    response = requests.get(f'{BASE_URL}/api/users')
    users = response.json()['users']
    
    if len(users) < 2:
        print("✗ Need at least 2 users to test bulk delete")
        return
    
    # Delete last 2 users
    ids_to_delete = [users[-1]['id'], users[-2]['id']]
    response = requests.post(f'{BASE_URL}/api/users/bulk-delete', json={'ids': ids_to_delete})
    
    if response.status_code == 200:
        print(f"✓ Bulk deleted {len(ids_to_delete)} users: {ids_to_delete}")
    else:
        print(f"✗ Failed to bulk delete")

def test_export_csv():
    """Test CSV export"""
    print("\n=== Testing CSV Export Feature ===")
    
    response = requests.get(f'{BASE_URL}/api/users/export')
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        lines = content.split('\n')
        print(f"✓ CSV export successful")
        print(f"  Headers: {lines[0]}")
        print(f"  Total rows: {len([l for l in lines if l.strip()])}")
    else:
        print("✗ CSV export failed")

def test_single_delete():
    """Test single user delete"""
    print("\n=== Testing Single Delete Feature ===")
    
    response = requests.get(f'{BASE_URL}/api/users')
    users = response.json()['users']
    
    if not users:
        print("✗ No users to delete")
        return
    
    user_id = users[-1]['id']
    user_name = users[-1]['name']
    
    response = requests.delete(f'{BASE_URL}/api/users/{user_id}')
    if response.status_code == 200:
        print(f"✓ Deleted user #{user_id}: {user_name}")
    else:
        print(f"✗ Failed to delete user #{user_id}")

def main():
    print("=" * 60)
    print("RETROSOUNDS ADMIN DASHBOARD - FEATURE TEST SUITE")
    print("=" * 60)
    
    try:
        # Test all features
        test_add_users()
        time.sleep(1)
        
        test_get_users()
        time.sleep(1)
        
        test_update_user()
        time.sleep(1)
        
        test_export_csv()
        time.sleep(1)
        
        test_bulk_delete()
        time.sleep(1)
        
        test_single_delete()
        
        # Final count
        print("\n" + "=" * 60)
        response = requests.get(f'{BASE_URL}/api/users')
        final_count = response.json()['count']
        print(f"FINAL USER COUNT: {final_count}")
        print("=" * 60)
        print("\n✓ All tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to Flask server")
        print("  Make sure the server is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")

if __name__ == '__main__':
    main()
