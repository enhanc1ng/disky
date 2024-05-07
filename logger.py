import datetime
from colorama import init, Fore

init(autoreset=True)

def info(msg, log=True):
    if not log: return
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    prefix = f"{Fore.LIGHTBLACK_EX}[{Fore.GREEN}DISKY{Fore.LIGHTBLACK_EX}]"
    msg_str = f"{Fore.WHITE}{msg}"
    print(f"{prefix} - {current_time} $ {msg_str}")

def error(msg, log=True):
    if not log: return
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    prefix = f"{Fore.LIGHTBLACK_EX}[{Fore.RED}DISKY{Fore.LIGHTBLACK_EX}]"
    msg_str = f"{Fore.LIGHTRED_EX}{msg}"
    print(f"{prefix} - {current_time} $ {msg_str}")