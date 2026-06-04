from datetime import datetime

# In-memory database
DB = {}

def create_user(user_id, name, telegram_username, phone_number):
    DB[user_id] = {
        "user_id": user_id,
        "name": name,
        "telegram_username": telegram_username,
        "phone_number": phone_number,
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "container_id": None,
        "pairing_code": None
    }
    return user_id

def get_user(user_id):
    return DB.get(user_id)

def get_user_by_telegram(telegram_username):
    for user in DB.values():
        if user["telegram_username"] == telegram_username:
            return user
    return None

def update_user_status(user_id, status):
    if user_id in DB:
        DB[user_id]["status"] = status
        DB[user_id]["updated_at"] = datetime.now().isoformat()

def update_user_container(user_id, container_id):
    if user_id in DB:
        DB[user_id]["container_id"] = container_id

def update_pairing_code(user_id, pairing_code):
    if user_id in DB:
        DB[user_id]["pairing_code"] = pairing_code

def get_all_users():
    return list(DB.values())