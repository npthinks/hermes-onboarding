import json
import os
from datetime import datetime

DB_FILE = "users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data: dict):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_user(
    user_id: str,
    name: str,
    telegram_username: str,
    phone_number: str
):
    db = load_db()
    db[user_id] = {
        "user_id": user_id,
        "name": name,
        "telegram_username": telegram_username,
        "phone_number": phone_number,
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "container_id": None,
        "pairing_code": None
    }
    save_db(db)
    return user_id

def get_user(user_id: str):
    db = load_db()
    return db.get(user_id)

def get_user_by_telegram(telegram_username: str):
    db = load_db()
    for user in db.values():
        if user["telegram_username"] == telegram_username:
            return user
    return None

def update_user_status(user_id: str, status: str):
    db = load_db()
    if user_id in db:
        db[user_id]["status"] = status
        db[user_id]["updated_at"] = datetime.now().isoformat()
        save_db(db)

def update_user_container(user_id: str, container_id: str):
    db = load_db()
    if user_id in db:
        db[user_id]["container_id"] = container_id
        save_db(db)

def update_pairing_code(user_id: str, pairing_code: str):
    db = load_db()
    if user_id in db:
        db[user_id]["pairing_code"] = pairing_code
        save_db(db)

def get_all_users():
    db = load_db()
    return list(db.values())