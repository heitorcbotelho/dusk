import datetime
import random
from dusk_cli.memory import load_name

def get_time() -> str:
    """
    Retorna uma saudação baseada no horário atual.
    """
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Bom dia"
    elif 12 <= hour < 18:
        return "Boa tarde"
    return "Boa noite"

def get_opening_phrase(program: str, name: str = "") -> str:
    """
    Retorna uma frase aleatória para abrir um programa.
    """
    phrases = [
        f"Abrindo {program}...",
        f"Claro! Iniciando {program}.",
        f"{program}? Ok!",
        f"Pode deixar {name}, abrindo {program} agora!" if name else f"Pode deixar, abrindo {program} agora!"
    ]
    return random.choice(phrases)

def get_greeting(name: str) -> str:
    """
    Retorna uma saudação personalizada para o usuário.
    """
    phrases_known = [
        f"Olá {name}!", 
        f"Você por aqui de novo, {name}? Como posso ajudar?",
        f"{get_time()}, {name}! Tudo certo?"
    ]
    phrases_new = [
        f"Muito prazer {name}, me chamo Dusk! Como posso ajudar?",
        f"Olá {name}, seja bem-vindo ao Dusk!"
    ]
    return random.choice(phrases_known if name else phrases_new)

def get_bye() -> str:
    """
    Retorna uma mensagem de despedida.
    """
    phrases = [
        "Até mais!", 
        f"{get_time()}! Se precisar, é só chamar.", 
        "Dusk saindo..."
    ]
    return random.choice(phrases)

def get_error() -> str:
    """
    Retorna uma mensagem de erro genérica para comandos não reconhecidos.
    """
    phrases = [
        "Desculpe, ainda não entendi esse comando.",
        "Hmm... ainda não aprendi isso.",
        "Esse comando não está nas minhas habilidades (ainda)."
    ]
    return random.choice(phrases)

def get_create_folder(folder_name: str) -> str:
    """
    Retorna uma mensagem confirmando a criação de uma pasta.
    """
    phrases = [
        f"Pasta '{folder_name}' criada com sucesso!",
        f"Tudo certo! A pasta '{folder_name}' foi criada."
    ]
    return random.choice(phrases)

def get_open_website(site_name: str) -> str:
    """
    Retorna uma mensagem confirmando a abertura de um site.
    """
    phrases = [
        f"Abrindo {site_name}...",
        f"Claro, acessando {site_name} agora mesmo."
    ]
    return random.choice(phrases)