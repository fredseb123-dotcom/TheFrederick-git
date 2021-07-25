"""
Doprovodné příkazy
"""

from datetime import datetime, date, timedelta
from time import sleep
import yaml


def time_now():
    """Zisk aktuálního času"""

    now = datetime.now() + timedelta(hours=6, minutes=2)
    time = now.strftime("%H:%M:%S") + date.today().strftime(" | %d-%m-%Y")
    return time


def load_cfg(item):
    """Zisk aktuálních konfiguračních dat"""

    try:
        with open("config/config.yml") as file:
            item = yaml.load(file, Loader=yaml.FullLoader)[item]
        return item
    except KeyError:
        print("Config >> Položka nenalezena")
    except FileNotFoundError:
        print("Config >> Configurační soubor nenalezen")
    return None

def load_radio(item):
    try:
        with open("config/radios.yml") as file:
            item = yaml.load(file, Loader=yaml.FullLoader)[item]
        return item
    except KeyError:
        print("Radios >> Položka nenalezena")
    except FileNotFoundError:
        print("Radios >> Configurační soubor nenalezen")
    return None

def chperm(roles, permisson):
    """Ověření práv pro provedení operace"""

    try:
        with open("config/perms.yml") as file:
            perm = yaml.load(file, Loader=yaml.FullLoader)[permisson]
            for role in roles:
                if role.id in perm:
                    return True
        return False
    except KeyError:
        print("Perms >> Položka nenalezena")
    except FileNotFoundError:
        print("Perms >> Soubor s právy nenalezen")

def start_seq():
    with open("images/logo.txt", "r") as file:
        img = file.readlines()

    coloring = {
        "*": "\u001b[38;5;172m*\u001b[0m",
        "@": "\u001b[37;1m@\u001b[0m",
        "%": "\u001b[30;1m%\u001b[0m",
        ".": "\u001b[38;5;224m&\u001b[0m",
        "&": "\u001b[38;5;223m&\u001b[0m",
    }

    final = []
    for row_num in range(0, len(img) - 1):
        final.append("".join([coloring[x] if x in coloring else x for x in img[row_num]]))
    for elem in final:
        print(elem, end="\r")
        sleep(0.05)
