from difflib import get_close_matches
import os
import subprocess
import json
from dusk_cli.ai.gemini_api import ask_gemini, make_response

DEBUG = True  # Ative para ver a resposta da IA
PROGRAM_PATHS_FILE = "data/program_paths.json"  # Arquivo JSON para armazenar os caminhos dos programas
def load_program_paths() -> dict:
    """
    Carrega os caminhos dos programas salvos no arquivo JSON.
    """
    try:
        with open(PROGRAM_PATHS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(make_response(f"Erro ao carregar os caminhos dos programas: {e}"))
        return {}

def save_program_paths(paths: dict) -> None:
    """
    Salva os caminhos dos programas no arquivo JSON.
    """
    try:
        with open(PROGRAM_PATHS_FILE, "w", encoding="utf-8") as file:
            json.dump(paths, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(make_response(f"Erro ao salvar os caminhos dos programas: {e}"))

def open_programs(command: str, name: str) -> None:
    """
    Abre programas com base no comando do usuário. Se o programa não for encontrado,
    solicita o caminho ao usuário e salva para uso futuro.
    """
    def find_executable_direct(name: str):
        try:
            result = subprocess.check_output(
                f"where {name}",
                shell=True,
                text=True,
                stderr=subprocess.DEVNULL
            )
            paths = result.strip().split("\n")
            return paths[0] if paths else None
        except subprocess.CalledProcessError:
            return None

    def find_shortcut_in_start_menu(program_name: str):
        start_menu_paths = [
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
        ]
        
        possible_matches = []

        for base_path in start_menu_paths:
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.lower().endswith('.lnk'):
                        possible_matches.append(os.path.join(root, file))
        
        shortcut_names = [os.path.splitext(os.path.basename(path))[0].lower() for path in possible_matches]
        close = get_close_matches(program_name.lower(), shortcut_names, n=1, cutoff=0.6)

        if close:
            idx = shortcut_names.index(close[0])
            return possible_matches[idx]
        
        return None

    def find_installed_program_path(program_name: str):
        possible_dirs = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            os.environ.get("ProgramW6432", r"C:\Program Files"),
        ]

        possible_matches = []
        
        for base_dir in possible_dirs:
            for root, dirs, files in os.walk(base_dir):
                for dir_name in dirs:
                    if program_name.lower() in dir_name.lower():
                        return os.path.join(root, dir_name)
                    else:
                        possible_matches.append(os.path.join(root, dir_name))
        
        folder_names = [os.path.basename(p).lower() for p in possible_matches]
        close = get_close_matches(program_name.lower(), folder_names, n=1, cutoff=0.6)
        
        if close:
            idx = folder_names.index(close[0])
            return possible_matches[idx]
        
        return None

    def find_executable_in_folder(folder: str, program_name: str):
        best_match = None
        for root, dirs, files in os.walk(folder):
            executables = [f for f in files if f.endswith(".exe")]
            if not executables:
                continue
            
            close = get_close_matches(program_name.lower(), [exe.lower() for exe in executables], n=1, cutoff=0.5)
            if close:
                best_match = os.path.join(root, close[0])
                break
        
        return best_match

    try:
        cleaned_command = command.lower().strip().replace("?", "").replace("abra", "").replace("dusk", "").strip()

        # Carrega os caminhos salvos
        program_paths = load_program_paths()

        # Verifica se o programa já está salvo
        if cleaned_command in program_paths:
            program_path = program_paths[cleaned_command]
            subprocess.Popen([program_path])
            print(make_response(f"Abrindo {cleaned_command} a partir do caminho salvo!", name))
            return

        # Tenta identificar o programa com o Gemini
        prompt = f"O usuário disse: '{cleaned_command}'. Qual programa você acha que ele quer abrir no Windows? Responda apenas com o nome curto (tipo 'calc.exe' ou 'notepad.exe') ou nome exato do aplicativo (como 'Steam', 'Telegram')."
        response = ask_gemini(prompt)
        program_name = response.strip()

        # 1. Tenta abrir diretamente
        program_path = find_executable_direct(program_name)
        if program_path:
            subprocess.Popen([program_path])
            print(make_response(f"Aberto {program_name}!", name))
            return

        # 2. Tenta abrir atalho do menu iniciar
        shortcut_path = find_shortcut_in_start_menu(program_name)
        if shortcut_path:
            subprocess.Popen(["explorer", shortcut_path])
            print(make_response(f"Aberto {program_name} pelo menu iniciar!", name))
            return

        # 3. Tenta procurar a instalação
        installed_path = find_installed_program_path(program_name)
        if installed_path:
            executable = find_executable_in_folder(installed_path, program_name)
            if executable:
                subprocess.Popen([executable])
                print(make_response(f"Aberto {program_name}!", name))
                return

        # Se não encontrar, solicita o caminho ao usuário
        make_response(f"Não encontrei o programa '{program_name}'.")
        user_path = input(f"Por favor, informe o caminho completo para o programa '{program_name}': ").strip()

        if os.path.isfile(user_path) and user_path.endswith(".exe"):
            program_paths[cleaned_command] = user_path
            save_program_paths(program_paths)
            subprocess.Popen([user_path])
            print(make_response(f"Executando {program_name} e salvando o caminho para uso futuro!", name))
        else:
            print(make_response("O caminho informado não é válido ou não é um executável.", name))

    except Exception as e:
        print(make_response(f"Erro ao abrir programa: {e}", name))
