import json
import os
import datetime
import re
import webbrowser
from dusk_cli.ai.gemini_api import ask_gemini, make_response
from dusk_cli.memory import load_name

name = load_name()
FOLDER_PATH = os.getenv("CREATE_FOLDER_PATH")

ASK_KEYWORDS = ["qual", "qual é", "meu", "minha"]
SAVE_KEYWORDS = ["é", "gosto de", "prefiro"]

URLS = {
    "google": "https://google.com",
    "youtube": "https://youtube.com",
    "wikipedia": "https://wikipedia.com",
}

def show_time() -> None:
    """
    Mostra a hora atual.
    """
    now = datetime.datetime.now().strftime("%H:%M")
    text = f"Agora são {now}"

    return make_response(text, name, "responda o horário no formato 24 horas")

def show_date() -> None:
    """
    Mostra a data atual.
    """
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    text = f"Hoje é {today}"
    return make_response(text, name, "responda a data no formato dia/mês/ano")

def create_folder(command: str) -> None:
    """
    Cria uma pasta na pasta determinada pelo usuário
    """
    try:
        base_path = os.path.expanduser(FOLDER_PATH)
        os.makedirs(base_path, exist_ok=True)

        parts = command.split()
        folder_name = parts[-1] if len(parts) > 2 else None  # Ex: "criar pasta teste"

        while True:
            if not folder_name:
                folder_name = input("Qual vai ser o nome da pasta?: ").strip()
            
            if not folder_name:
                print(make_response("Você não pode criar uma pasta sem nome.", name, "Você está criando uma pasta no computador"))
                continue

            full_path = os.path.join(base_path, folder_name)

            if not os.path.exists(full_path):
                os.makedirs(full_path)
                print(make_response(f"A pasta {folder_name} foi criada com sucesso!", name, "Você criou uma nova pasta"))
                break
            else:
                print(make_response(f"A pasta {folder_name} já existe. Escolha outro nome.", name, "Você está criando uma pasta no computador"))
                folder_name = None
    except Exception as e:
        print(make_response(f"Ocorreu um erro ao tentar criar a pasta: {e}", name, "Erro durante a criação de uma pasta no computador"))

def open_website(command: str) -> None:
    """
    Abre um site baseado no comando fornecido, utilizando o navegador padrão.
    """
    try:
        # Extrai nome do site
        prompt_site = f"""
        Você é um assistente que extrai apenas o nome do site solicitado em um comando.

        Comando do usuário: {command}

        Retorne só o nome, como 'google', 'youtube', etc.
        """
        site_name = ask_gemini(prompt_site.strip().lower()).strip()
        url = f"https://{site_name}.com"

        # Detecta se é para abrir em modo anônimo
        prompt_anon = f"""
        O usuário quer abrir o site em modo anônimo?

        Comando: "{command}"

        Responda apenas 'sim' ou 'não'.
        """
        anon_response = ask_gemini(prompt_anon.strip().lower()).strip()

        if "sim" in anon_response.lower():
            print(make_response(
                f"Modo anônimo ainda não é suportado com o navegador padrão. Abrindo normalmente...",
                name,
                "Futuramente o Dusk poderá detectar o navegador e abrir corretamente em modo privado."
            ))

        webbrowser.open_new(url)
        print(make_response(f"O site {site_name} está sendo aberto.", name))

    except Exception as e:
        print(make_response(f"Ocorreu um erro ao abrir o site: {e}", name, "Erro ao abrir site no navegador."))

def interpret_command(command: str) -> dict | None:
    prompt = f"""
    Você é um sistema de interpretação de comandos do assistente Dusk.

    Frase: "{command}"

    Responda APENAS com um JSON válido com:
    - "acao": uma das ações possíveis: ["mostrar_hora", "mostrar_data", "criar_pasta", "abrir_programa", "abrir_site", "sair", "ajuda", "preferencias", "pesquisa_ia"]
    - "parametros": um dicionário com as informações relevantes para executar a ação.

    Exemplos:
    Entrada: "que horas são?"
    Saída: {{ "acao": "mostrar_hora" }}

    Entrada: "crie uma pasta chamada imagens"
    Saída: {{ "acao": "criar_pasta", "parametros": {{ "nome": "imagens" }} }}

    NÃO adicione nenhuma explicação ou texto extra.
    """.strip()

    try:
        response = ask_gemini(prompt)
        # Extrai só o JSON da resposta
        json_text = re.search(r'\{.*\}', response, re.DOTALL)
        if json_text:
            return json.loads(json_text.group())
        return None
    except Exception:
        return None

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
