import datetime

def save_log(user_msg, bot_reply):
    now = datetime.datetime.now().strftime("[%d/%m/%Y %H:%M]")
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{now} - User: {user_msg}\n")
        log_file.write(f"{now} - Dusk: {bot_reply}\n")