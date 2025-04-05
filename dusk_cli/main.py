from dusk_cli.command import open_programs, show_time, show_date
from dusk_cli.memory import save_name, load_name

name = load_name()
if name is None:
    name = input("Olá, qual é o seu nome?: ")
    save_name(name)
    print(f"Olá {name}, me chamo Dusk, como posso ajudar?")
else:
    print(f"Olá {name}, como posso ajudar?")

while True:
    command = input("> ").lower().strip()
    if "abrir" in command:
        open_programs(command)
    elif "horas" in command:
        show_time()
    elif "hoje" in command:
        show_date()
    elif "sair" in command:
        print("Se precisar é só chamar :)")
        break
    else:
        print("Não entendi o comando.")

    print("Precisa de mais alguma coisa?")