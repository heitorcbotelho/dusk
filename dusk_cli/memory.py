import json
import os

# Caminho para o arquivo na pasta "data"
DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "file.json")

# Garante que a pasta "data" exista
os.makedirs(DATA_DIR, exist_ok=True)

def save_name(name):
    with open(FILE_PATH, "w") as file:
        json.dump({"name": name}, file, indent=4)

def load_name():
    try:
        with open(FILE_PATH, "r") as file:
            info = json.load(file)
            return info["name"]

    except FileNotFoundError:
        return None

    except json.JSONDecodeError:
        return None


