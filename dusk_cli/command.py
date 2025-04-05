import subprocess
import datetime
from dusk_cli.memory import load_name

programs = {
    "calculadora": "calc.exe",
    "bloco": "notepad.exe",
}

def open_programs(command):
    com = command.split()[-1].lower()
    if com in programs:
        try:
            subprocess.Popen([programs[com]])
            print(f"Certo {load_name()}, abrindo {com}...")
        except Exception as e:
            print(f"Houve um erro ao tentar abrir {com}: {e}")

    else:
        print(f"Desculpe {load_name()}, ainda não sei abrir {com}.")

def show_time():
    now = datetime.datetime.now().strftime("%H:%M")
    print(f"Agora são {now}")

def show_date():
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    print(f"Hoje é {today}")


