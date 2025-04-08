import json
import os

DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "file.json")
os.makedirs(DATA_DIR, exist_ok=True)

def save_name(name):
    data = load_data()
    data["name"] = name
    save_data(data)

def load_name():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
            return data.get("name")
    return None

def load_data():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

def save_preference(user_name, key, value):
    data = load_data()
    if user_name not in data:
        data[user_name] = {"preferences": {}}
    if "preferences" not in data[user_name]:
        data[user_name]["preferences"] = {}
    data[user_name]["preferences"][key] = value
    save_data(data)

def get_preference(user_name, key):
    data = load_data()
    return data.get(user_name, {}).get("preferences", {}).get(key)