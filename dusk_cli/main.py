def main():
    from dusk_cli.command import open_programs, show_time, show_date, create_folder, open_website, handle_preferences
    from dusk_cli.memory import save_name, load_name, save_preference
    from dusk_cli.responses import get_greeting, get_bye, get_error

    open_programs_keywords = ["abrir", "abre", "executar", "iniciar", "começar", "rodar", "ligar", "execute", "abra"]
    hour_keywords = ["horas", "relógio", "que horas", "me diz as horas", "são quantas horas", "tempo", "agora"]
    date_keywords = ["data", "hoje", "dia", "qual é a data", "que dia é hoje", "data de hoje"]
    getout_keyword = ["sair", "fechar", "encerrar", "até mais", "tchau", "desligar", "finalizar"]
    create_folder_keywords = ["criar pasta", "crie uma pasta", "adicionar pasta"]
    preferences_keywords = ["preferência", "gosto", "favorita", "favorito"]

    # Inicialização do nome do usuário
    try:
        name = load_name()
        if name is None or name.strip() == "":
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
            command = input("> ").lower().strip()
            
            if not command:
                continue
                
            # Verifica se o usuário deseja sair
            if any(k in command for k in getout_keyword):
                print(get_bye())
                break
                
            # Processar comandos
            if any(k in command for k in create_folder_keywords):
                create_folder(command)
            elif "site" in command:
                open_website(command)
            elif any(k in command for k in open_programs_keywords):
                open_programs(command, name)
            elif any(k in command for k in hour_keywords):
                show_time()
            elif any(k in command for k in date_keywords):
                show_date()
            elif any(k in command for k in preferences_keywords):
                handle_preferences(command, name)
            else:
                print(get_error())
                
            print("Precisa de mais alguma coisa?")
            
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            print("Vamos tentar novamente.")

if __name__ == "__main__":
    main()
