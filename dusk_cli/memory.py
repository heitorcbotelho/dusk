import json
import os

DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "file.json")

def ensure_data_dir():
    """Garante que o diretório de dados existe"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório de dados: {e}")
        return False

def save_name(name):
    """Salva o nome do usuário"""
    if not ensure_data_dir():
        return False
        
    try:
        data = load_data()
        data["name"] = name
        return save_data(data)
    except Exception as e:
        print(f"Erro ao salvar nome: {e}")
        return False

def load_name():
    """Carrega o nome do usuário"""
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("name")
    except Exception as e:
        print(f"Erro ao carregar nome: {e}")
    return None

def load_data():
    """Carrega todos os dados do arquivo"""
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Erro ao carregar dados: {e}")
    return {}

def save_data(data):
    """Salva todos os dados no arquivo"""
    if not ensure_data_dir():
        return False
        
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False

def save_preference(user_name, key, value):
    """Salva uma preferência do usuário"""
    try:
        data = load_data()
        if user_name not in data:
            data[user_name] = {"preferences": {}}
        if "preferences" not in data[user_name]:
            data[user_name]["preferences"] = {}
        data[user_name]["preferences"][key] = value
        return save_data(data)
    except Exception as e:
        print(f"Erro ao salvar preferência: {e}")
        return False

def get_preference(user_name, key):
    """Obtém uma preferência do usuário"""
    try:
        data = load_data()
        return data.get(user_name, {}).get("preferences", {}).get(key)
    except Exception as e:
        print(f"Erro ao obter preferência: {e}")
        return None