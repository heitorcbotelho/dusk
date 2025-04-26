from difflib import get_close_matches
import os
import subprocess
from dusk_cli.ai.gemini_api import ask_gemini

DEBUG = True  # Ative para ver a resposta da IA
def open_programs(command: str):
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

        prompt = f"O usuário disse: '{cleaned_command}'. Qual programa você acha que ele quer abrir no Windows? Responda apenas com o nome curto (tipo 'calc.exe' ou 'notepad.exe') ou nome exato do aplicativo (como 'Steam', 'Telegram')."
        response = ask_gemini(prompt)
        program_name = response.strip()
        
        # print(f"[DEBUG Gemini] Programa identificado: {program_name}")

        # 1. Tenta abrir diretamente
        program_path = find_executable_direct(program_name)
        if program_path:
            subprocess.Popen([program_path])
            print(f"Abrindo {program_name}!")
            return

        # 2. Tenta abrir atalho do menu iniciar
        shortcut_path = find_shortcut_in_start_menu(program_name)
        if shortcut_path:
            subprocess.Popen(["explorer", shortcut_path])
            print(f"Abrindo {program_name} pelo menu iniciar!")
            return

        # 3. Tenta procurar a instalação
        installed_path = find_installed_program_path(program_name)
        if installed_path:
            print(f"[DEBUG] Pasta encontrada: {installed_path}")
            executable = find_executable_in_folder(installed_path, program_name)
            if executable:
                subprocess.Popen([executable])
                print(f"Abrindo {program_name}!")
                return

        print(f"Não encontrei o programa '{program_name}' instalado no sistema.")
    except Exception as e:
        print(f"Erro ao abrir programa: {e}")
