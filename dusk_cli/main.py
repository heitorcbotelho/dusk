from dusk_cli.ai.gemini_api import make_response, think
from dusk_cli.command import (
    interpret_command, show_time, show_date, create_folder,
    open_website, show_help
)
from dusk_cli.program_launcher import open_programs
from dusk_cli.memory import save_name, load_name
from dusk_cli.log import save_log

def handle_command(action, params, command, name):
    actions = {
        "mostrar_hora": lambda: (show_time(), "Mostrou a hora atual."),
        "mostrar_data": lambda: (show_date(), "Mostrou a data atual."),
        "criar_pasta": lambda: (
            create_folder(params.get("nome", "Nova Pasta")),
            f"Folder '{params.get('nome', 'Nova Pasta')}' created."
        ),
        "abrir_programa": lambda: (
            open_programs(params.get("nome"), name),
            f"Programa '{params.get('nome')}' aberto."
        ),
        "abrir_site": lambda: (
            open_website(command),
            "Site aberto."
        ),
        "pesquisa_ia": lambda: (
            think(params.get("pergunta", command), name),
            None
        ),
        "ajuda": lambda: (
            show_help(command),
            "Mostrou a lista de comandos."
        ),
        "sair": lambda: (
            make_response("Até logo!", name, "se despediu"),
            "Saiu do programa."
        ),
    }
    if action in actions:
        result, log_msg = actions[action]()
        if result is not None:
            print(result)
        if log_msg:
            save_log(command, log_msg)
        return action == "sair"
    else:
        print(make_response("Desculpe, não entendi o comando.", name))
        save_log(command, "Comando não reconhecido.")
        return False

def main_loop(name):
    print(make_response("Olá, como posso ajudar?", name, "lembre-se de ser amigável"))
    while True:
        try:
            command = input("> ").lower().strip()
            if not command:
                continue
            interpreted = interpret_command(command)
            if not interpreted:
                print(make_response("Desculpe, não entendi o comando.", name))
                save_log(command, "Comando não reconhecido.")
                continue
            action = interpreted.get("acao")
            params = interpreted.get("parametros", {})
            if handle_command(action, params, command, name):
                break
            if action != "sair":
                print(make_response("Posso ajudar com mais alguma coisa?", name))
        except Exception as e:
            print(f"Houve um erro: {e}")
            save_log("ERROR", str(e))
            print("Vamos tentar novamente.")

def main():
    try:
        name = load_name() or input("Olá, qual é o seu nome?: ").strip() or "user"
        save_name(name)
    except Exception as e:
        print(f"Houve um problema para carregar o nome: {e}")
        name = "user"
    main_loop(name)

if __name__ == "__main__":
    main()