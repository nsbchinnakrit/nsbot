import sys
import os
import logging
import importlib
import argparse
import threading
import signal  # เพิ่มการ import signal
import keyboard
from Module.logsystem import MyLog

# ฟังก์ชันสำหรับจัดการ signal
def signal_handler(sig, frame):
    logging.warning("[EXIT] Ctrl+C pressed — stopping the bot.")
    os._exit(0)

def create_file(pid, data='0'):
    try:
        temp_path = f"runprocess/temp{pid}.txt"
        with open(temp_path, "w") as file:
            file.write(data)
    except Exception as error:
        logging.error("[ERROR] create_file: %s", error)

def dynamic_import(module_path, class_name):
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except Exception as e:
        logging.error("[ERROR] Could not import %s from %s: %s", class_name, module_path, e)
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description="NSBot Launcher")
    parser.add_argument("game_mode", type=str, help="Game mode to run")
    parser.add_argument("server", type=str, help="Server name")
    parser.add_argument("window_name", type=str, help="Window title")
    parser.add_argument("before_total", type=int)
    parser.add_argument("total", type=int)
    parser.add_argument("bondling_mode", type=str)
    parser.add_argument("pact_settings", type=str)
    parser.add_argument("crystal_use", type=str)
    parser.add_argument("tomb", type=str)
    parser.add_argument("snowball", type=str)
    parser.add_argument("azure", type=str)
    parser.add_argument("kuro", type=str)
    parser.add_argument("mark_boss", type=str)
    return parser.parse_args()

def main():
    # ลงทะเบียน signal handler สำหรับ SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    args = parse_args()
    pid = os.getpid()

    # Logging setup
    MyLog.init(loglv='DEBUG')
    logging.debug("GameMode: [%s], Server: [%s], Total Rounds: [%s]", args.game_mode, args.server, args.total)

    # Mapping for game modes (module path, class name)
    game_modes = {
        "SingleSoul": ("GameMode.SingleSoul", "SingleSoul"),
        "Soul": ("GameMode.Soul", "Soul"),
        "Explore": ("GameMode.Explore", "Explore"),
        "SingleExplore": ("GameMode.SingleExplore", "SingleExplore"),
        "RealmRaid": ("GameMode.RealmRaid", "RealmRaid"),
        "RealmRaidW3F3": ("GameMode.RealmRaidW3F3", "RealmRaidW3F3"),
        "GuildRealmRaid": ("GameMode.GuildRealmRaid", "GuildRealmRaid"),
        "Explor3Realm": ("GameMode.Explor3Realm", "Explor3Realm"),
        "Explor3RealmW3F3": ("GameMode.Explor3RealmW3F3", "Explor3RealmW3F3"),
        "Event": ("GameMode.Event", "Event"),
        "Bondling": ("GameMode.Bondling", "Bondling"),
    }

    if args.game_mode not in game_modes:
        logging.error("Invalid game mode: %s", args.game_mode)
        sys.exit(1)

    module_path, class_name = game_modes[args.game_mode]
    GameModeClass = dynamic_import(module_path, class_name)

    instance = GameModeClass(
        args.server,
        args.window_name,
        args.before_total,
        args.total,
        pid,
        args.bondling_mode,
        args.pact_settings,
        args.crystal_use,
        args.tomb,
        args.snowball,
        args.azure,
        args.kuro,
        args.mark_boss
    )
    
    try:
        instance.start()
        
        # ใช้ while loop เพื่อให้โปรแกรมหลักยังคงทำงานและสามารถรับ signal ได้
        while instance.is_alive():
            instance.join(0.1)  # join with timeout เพื่อให้โปรแกรมสามารถรับ interrupt ได้
            
    except KeyboardInterrupt:
        logging.warning("[EXIT] Ctrl+C pressed — stopping the bot.")
        os._exit(0)

if __name__ == "__main__":
    main()