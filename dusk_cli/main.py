from dusk_cli.command import interpret_command
from dusk_cli.program_launcher import open_programs


def main():
    from dusk_cli.command import (
        show_time, show_date, create_folder, open_website,
        handle_preferences, show_help
    )
    from dusk_cli.memory import save_name, load_name
    from dusk_cli.responses import get_greeting, get_bye, get_error
    from dusk_cli.log import save_log
    from dusk_cli.ai.gemini_api import think

    try:
        name = load_name() or input("Olá, qual é o seu nome?: ").strip() or "user"
        save_name(name)
    except Exception as e:
        print(f"Houve um problema para carregar o nome: {e}")
        name = "user"

    print(get_greeting(name))

    while True:
        try:
            command = input("> ").lower().strip()
            if not command:
                continue

            interpreted = interpret_command(command)
            if not interpreted:
                error = get_error()
                print(error)
                save_log(command, error)
                continue

            action = interpreted.get("acao")
            params = interpreted.get("parametros", {})

            if action == "mostrar_hora":
                print(show_time())
                save_log(command, "Mostrou a hora atual.")

            elif action == "mostrar_data":
                print(show_date())
                save_log(command, "Mostrou a data atual.")

            elif action == "criar_pasta":
                folder_name = params.get("nome", "Nova Pasta")
                create_folder(folder_name)
                save_log(command, f"Folder '{folder_name}' created.")

            elif action == "abrir_programa":
                program_name = params.get("nome")
                open_programs(program_name)
                save_log(command, f"Programa '{program_name}' aberto.")

            elif action == "abrir_site":
                open_website(command)
                save_log(command, "Site aberto.")

            elif action == "preferencias":
                response = handle_preferences(command, name)
                print(response)
                save_log(command, "Manipulou as preferências do usuário.")

            elif action == "pesquisa_ia":
                question = params.get("pergunta", command)
                response = think(question, name)
                print(response)
                save_log(command, response)

            elif action == "ajuda":
                show_help(command)
                save_log(command, "Mostrou a lista de comandos.")

            elif action == "sair":
                bye = get_bye()
                print(bye)
                save_log(command, bye)
                break

            else:
                error = get_error()
                print(error)
                save_log(command, error)

            print("Posso ajudar com mais alguma coisa?")

        except Exception as e:
            print(f"Houve um erro: {e}")
            save_log("ERROR", str(e))
            print("Vamos tentar novamente.")

if __name__ == "__main__":
    main()