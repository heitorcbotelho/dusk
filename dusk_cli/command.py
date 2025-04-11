import os
import subprocess
import datetime
import webbrowser
from dusk_cli.responses import get_opening_phrase, get_create_folder, get_open_website
from dusk_cli.memory import save_preference, get_preference, load_name

PROGRAMS = {
    "calculadora": "calc.exe",
    "bloco": "notepad.exe",
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "obs": r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
}

ASK_KEYWORDS = ["qual", "qual é", "meu", "minha"]
SAVE_KEYWORDS = ["é", "gosto de", "prefiro"]

URLS = {
    "google": "https://google.com",
    "youtube": "https://youtube.com",
    "wikipedia": "https://wikipedia.com",
}

def open_programs(command: str, name: str = "") -> None:
    """
    Abre um programa baseado no comando fornecido.
    """
    try:
        program_key = command.split()[-1].lower()
        if program_key in PROGRAMS:
            subprocess.Popen([PROGRAMS[program_key]])
            print(get_opening_phrase(program_key, name))
        else:
            user_name = name or load_name() or ""
            print(f"Desculpe {user_name}, ainda não sei abrir {program_key}.")
    except IndexError:
        print("Por favor, especifique qual programa deseja abrir.")
    except Exception as e:
        print(f"Houve um erro ao tentar abrir o programa: {e}")

def show_time() -> None:
    """
    Mostra a hora atual.
    """
    now = datetime.datetime.now().strftime("%H:%M")
    print(f"Agora são {now}")

def show_date() -> None:
    """
    Mostra a data atual.
    """
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    print(f"Hoje é {today}")

def create_folder(command: str) -> None:
    """
    Cria uma pasta na pasta determinada pelo usuário
    """
    try:
        base_path = os.path.expanduser("~/Desktop/Dusk pastas")
        os.makedirs(base_path, exist_ok=True)

        parts = command.split()
        folder_name = parts[-1] if len(parts) > 2 else None  # Ex: "criar pasta teste"

        while True:
            if not folder_name:
                folder_name = input("Qual vai ser o nome da pasta?: ").strip()
            
            if not folder_name:
                print("O nome da pasta não pode ser vazio.")
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

def open_website(command: str) -> None:
    """
    Abre um site baseado no comando fornecido.
    """
    try:
        words = command.split()
        if "site" not in words:
            print("Por favor, especifique qual site deseja abrir.")
            return
            
        site_index = words.index("site")
        if site_index + 1 >= len(words):
            print("Por favor, especifique qual site deseja abrir.")
            return
            
        site_name = words[site_index + 1].lower()

        if site_name in URLS:
            webbrowser.open(URLS[site_name])
        else:
            url = f"https://{site_name}.com"
            webbrowser.open(url)
        print(get_open_website(site_name))
    except Exception as e:
        print(f"Não consegui abrir o site: {e}")

def clean_text(text: str) -> str:
    """
    Limpa o texto removendo caracteres especiais e espaços desnecessários.
    """
    return text.replace("?", "").strip().lower()

def is_question(command: str) -> bool:
    """
    Determina se o comando é uma pergunta.
    """
    question_words = ["qual", "quais", "o que", "quem", "quando", "como", "onde"]
    return any(command.startswith(q) for q in question_words)

def extract_key_value(command: str) -> tuple[str, str]:
    """
    Extrai a chave e o valor de um comando de preferência.
    """
    if " é " in command:
        parts = command.split(" é ")
        if len(parts) == 2:
            key_raw = parts[0].strip().replace("meu", "").replace("minha", "").replace("favorito", "").replace("favorita", "")
            key = key_raw.strip().replace(" ", "_")
            value = parts[1].strip()
            return key, value
    return None, None

def extract_key_from_question(command: str) -> str:
    """
    Extrai a chave de uma pergunta sobre preferências.
    """
    question = command.replace("qual é", "").replace("meu", "").replace("minha", "").replace("favorito", "").replace("favorita", "")
    key = question.strip().replace(" ", "_")
    return key

def handle_preferences(command: str, user_name: str) -> None:
    """
   Registra ou recupera preferências do usuário.
    """
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

def show_help(command):
    """
    Mostra uma lista de comandos disponíveis.
    """
    print("Aqui estão algumas coisas que posso fazer:")
    print("- Criar pastas")
    print("- Abrir programas")
    print("- Mostrar a hora")
    print("- Mostrar a data")
    print("- Abrir sites")
    print("- Salvar e recuperar preferências pessoais")