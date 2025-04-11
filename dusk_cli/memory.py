import json
import os

# Constants
DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "file.json")

def ensure_data_dir() -> bool:
    """
    Se o diretório de dados não existir, cria o diretório.
    Retorna True se o diretório foi criado ou já existe, False se houve um erro.
    """
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório de dados: {e}")
        return False

def load_data() -> dict:
    """
    Carrega todos os dados do arquivo JSON.
    Retorna um dicionário com os dados ou um dicionário vazio se houver erro.
    Se o arquivo não existir, cria um novo arquivo JSON vazio.
    """
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Erro ao carregar dados: {e}")
    return {}

def save_data(data: dict) -> bool:
    """
    Salva os dados no arquivo JSON.
    Retorna True se os dados foram salvos com sucesso, False se houve erro.
    Se o diretório de dados não existir, tenta criá-lo.
    """
    if not ensure_data_dir():
        return False

    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False

def save_name(name: str) -> bool:
    """
    Salva o nome do usuário no arquivo JSON.
    """
    if not ensure_data_dir():
        return False

    try:
        data = load_data()
        data["name"] = name
        return save_data(data)
    except Exception as e:
        print(f"Erro ao salvar nome: {e}")
        return False

def load_name() -> str | None:
    """
    Carrega o nome do usuário do arquivo JSON.
    """
    try:
        data = load_data()
        return data.get("name")
    except Exception as e:
        print(f"Erro ao carregar nome: {e}")
    return None

def save_preference(user_name: str, key: str, value: str) -> bool:
    """
    Salva a preferência do usuário no arquivo JSON.
    """
    try:
        data = load_data()
        if user_name not in data:
            data[user_name] = {"preferences": {}}
        data[user_name]["preferences"][key] = value
        return save_data(data)
    except Exception as e:
        print(f"Erro ao salvar preferência: {e}")
        return False

def get_preference(user_name: str, key: str) -> str | None:
    """
    Retorna a preferência do usuário do arquivo JSON.
    """
    try:
        data = load_data()
        return data.get(user_name, {}).get("preferences", {}).get(key)
    except Exception as e:
        print(f"Erro ao obter preferência: {e}")
        return None