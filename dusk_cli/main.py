def main():
    """
    Função principal para lidar com comandos e interações do usuário.
    """
    from dusk_cli.command import (
        open_programs, show_time, show_date, create_folder, open_website, handle_preferences, show_help
    )
    from dusk_cli.memory import save_name, load_name
    from dusk_cli.responses import get_greeting, get_bye, get_error
    from dusk_cli.log import save_log
    from dusk_cli.ai.gemini_api import ask_gemini, think

    # Palavras-chave para identificar comandos
    OPEN_PROGRAMS_KEYWORDS = ["abrir", "abre", "executar", "iniciar", "começar", "rodar", "ligar", "execute", "abra"]
    HOUR_KEYWORDS = ["horas", "relógio", "que horas", "me diz as horas", "são quantas horas", "tempo", "agora"]
    DATE_KEYWORDS = ["data", "hoje", "dia", "qual é a data", "que dia é hoje", "data de hoje"]
    EXIT_KEYWORDS = ["sair", "fechar", "encerrar", "até mais", "tchau", "desligar", "finalizar"]
    CREATE_FOLDER_KEYWORDS = ["criar pasta", "crie uma pasta", "adicionar pasta"]
    PREFERENCES_KEYWORDS = ["preferência", "gosto", "favorita", "favorito"]

    # Inicialização do nome do usuário
    try:
        name = load_name()
        if not name or name.strip() == "":
            name = input("Olá, qual é o seu nome?: ").strip()
            if name:
                save_name(name)
            else:
                name = "usuário"
                save_name(name)
    except Exception as e:
        print(f"Houve um problema ao carregar seu nome: {e}")
        name = "usuário"

    print(get_greeting(name))

    while True:
        try:
            # Recebe o comando do usuário
            command = input("> ").lower().strip()
            if not command:
                continue

            # Checa se o comando é para sair
            if any(keyword in command for keyword in EXIT_KEYWORDS):
                bye_message = get_bye()
                print(bye_message)
                save_log(command, bye_message)
                break

            # Comandos
            if any(keyword in command for keyword in CREATE_FOLDER_KEYWORDS):
                create_folder(command)
                save_log(command, "Folder created successfully.")
            elif "site" in command:
                open_website(command)
                save_log(command, "Website opened successfully.")
            elif any(keyword in command for keyword in OPEN_PROGRAMS_KEYWORDS):
                open_programs(command, name)
                save_log(command, "Program opened successfully.")
            elif any(keyword in command for keyword in HOUR_KEYWORDS):
                show_time()
                save_log(command, "Displayed current time.")
            elif any(keyword in command for keyword in DATE_KEYWORDS):
                show_date()
                save_log(command, "Displayed current date.")
            elif any(keyword in command for keyword in PREFERENCES_KEYWORDS):
                handle_preferences(command, name)
                save_log(command, "Handled user preferences.")
            elif any(keyword in command for keyword in ["ajuda", "help"]):
                show_help(command)
                save_log(command, "Displayed help information.")
            elif command.startswith("ia") or command.startswith("pesquisar"):
                question = command.replace("ia", "").replace("pesquisar", "").strip()
                response = think(question, name)
                print(response)
                save_log(command, response)

            else:
                error_message = get_error()
                print(error_message)
                save_log(command, error_message)

            print("Precisa de mais alguma coisa?")

        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            save_log("ERROR", str(e))
            print("Vamos tentar novamente.")

if __name__ == "__main__":
    main()
