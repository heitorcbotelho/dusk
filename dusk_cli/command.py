import os
import subprocess
import datetime
import webbrowser
from dusk_cli.responses import get_opening_phrase, get_create_folder, get_open_website
from dusk_cli.memory import save_preference, get_preference, load_name

programs = {
    "calculadora": "calc.exe",
    "bloco": "notepad.exe",
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "obs": r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
}

ask_keywords = ["qual", "qual é", "meu", "minha"]
save_keywords = ["é", "gosto de", "prefiro"]

def open_programs(command, name=""):
    try:
        com = command.split()[-1].lower()
        if com in programs:
            try:
                subprocess.Popen([programs[com]])
                print(get_opening_phrase(com, name))
            except Exception as e:
                print(f"Houve um erro ao tentar abrir {com}: {e}")
        else:
            user_name = name or load_name() or ""
            print(f"Desculpe {user_name}, ainda não sei abrir {com}.")
    except IndexError:
        print("Por favor, especifique qual programa deseja abrir.")

def show_time():
    now = datetime.datetime.now().strftime("%H:%M")
    print(f"Agora são {now}")

def show_date():
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    print(f"Hoje é {today}")

def create_folder(command):
    try:
        base_path = os.path.expanduser("~/Desktop/Dusk pastas")
        os.makedirs(base_path, exist_ok=True)

        parts = command.split()
        folder_name = parts[-1] if len(parts) > 2 else None #Ex: "criar pasta teste"

        while True:
            if not folder_name:
                folder_name = input("Qual vai ser o nome da pasta?: ")
                
            if not folder_name.strip():
                print("O nome da pasta não pode ser vazio.")
                folder_name = None
                continue

            full_path = os.path.join(base_path, folder_name)

            if not os.path.exists(full_path):
                os.makedirs(full_path)
                print(get_create_folder(folder_name))
                break
            else:
                print(f"A pasta {folder_name} já existe, escolha outro nome.")
                folder_name = None
    except Exception as e:
        print(f"Ocorreu um erro ao criar a pasta: {e}")

def open_website(command):
    urls = {
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "wikipedia": "https://wikipedia.com"
    }

    try:
        words = command.split()
        if "site" not in words:
            print("Por favor, especifique qual site deseja abrir.")
            return
            
        site_index = words.index("site")
        if site_index + 1 >= len(words):
            print("Por favor, especifique qual site deseja abrir.")
            return
            
        site_name = words[site_index + 1]

        if site_name in urls:
            webbrowser.open(urls[site_name])
        else:
            url = f"https://{site_name}.com"
            webbrowser.open(url)
        print(get_open_website(site_name))

    except Exception as e:
        print(f"Não consegui abrir o site: {e}")

def clean_text(text):
    return text.replace("?", "").strip().lower()

def is_question(command):
    question_words = ["qual", "quais", "o que", "quem", "quando", "como", "onde"]
    return any(command.startswith(q) for q in question_words)

def extract_key_value(command):
    if " é " in command:
        parts = command.split(" é ")
        if len(parts) == 2:
            key_raw = parts[0].strip().replace("meu", "").replace("minha", "").replace("favorito", "").replace("favorita", "")
            key = key_raw.strip().replace(" ", "_")
            value = parts[1].strip()
            return key, value
    return None, None

def extract_key_from_question(command):
    question = command.replace("qual é", "").replace("meu", "").replace("minha", "").replace("favorito", "").replace("favorita", "")
    key = question.strip().replace(" ", "_")
    return key

def handle_preferences(command, user_name):
    command = clean_text(command)

    if is_question(command):
        key = extract_key_from_question(command)
        value = get_preference(user_name, key)
        if value:
            print(f"Sua {key.replace('_', ' ')} é {value}.")
        else:
            print(f"Ainda não sei qual é sua {key.replace('_', ' ')}, {user_name}.")
        return

    key, value = extract_key_value(command)
    if key and value:
        save_preference(user_name, key, value)
        print(f"Ok {user_name}, eu salvei sua {key.replace('_', ' ')} como {value}.")
    else:
        print("Não entendi. Pode repetir de outra forma?")