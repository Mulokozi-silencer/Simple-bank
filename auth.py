import json
import hashlib
import os

USER_DB = "database.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, 'w') as f:
            json.dump({}, f)
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, 'w') as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = {
        "password": hash_password(password),
        "balance": 0.0,
        "transactions": []
    }
    save_users(users)
    return True, "Registration successful."

def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    print("DEBUG:", username, hashed)
    
    if username in users:
        print("DEBUG STORED:", users[username]["password"])
    
    if username in users and users[username]["password"] == hashed:
        return True, users[username]
    return False, "Invalid username or password."

def get_user_data(username):
    users = load_users()
    return users.get(username, None)

def update_user_data(username, data):
    users = load_users()
    users[username] = data
    save_users(users)

