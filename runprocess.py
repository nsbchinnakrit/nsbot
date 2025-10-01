#!/usr/bin/env python3
"""
runprocess.py – Improved launcher for NSBot

* Logs **all** uncaught exceptions (main thread + every child thread).
* Keeps graceful Ctrl‑C handling.
* Uses logging.exception for richer error details in caught blocks.

Save over the old runprocess.py or keep side‑by‑side; both `auto‑py‑to‑exe` and
PyInstaller will still collect the hidden imports thanks to explicit imports
at the top of the file.
"""

from __future__ import annotations

import argparse
import importlib
import logging
import os
import signal
import sys
import threading
from pathlib import Path

# Third‑party / internal modules
from Module.loadconfig import config
from Module.logsystem import MyLog

# Explicit imports so PyInstaller sees them as hidden‑imports automatically
import GameMode.SingleSoul  # noqa: F401 – hidden import
import GameMode.Soul  # noqa: F401 – hidden import
import GameMode.Explore  # noqa: F401 – hidden import
import GameMode.SingleExplore  # noqa: F401 – hidden import
import GameMode.RealmRaid  # noqa: F401 – hidden import
import GameMode.RealmRaidW3F3  # noqa: F401 – hidden import
import GameMode.GuildRealmRaid  # noqa: F401 – hidden import
import GameMode.Explor3Realm  # noqa: F401 – hidden import
import GameMode.Explor3RealmW3F3  # noqa: F401 – hidden import
import GameMode.Event  # noqa: F401 – hidden import
import GameMode.Bondling  # noqa: F401 – hidden import

# --------------------------------------------------------------------------- #
#                         Utilities                                           #
# --------------------------------------------------------------------------- #

def setup_global_exception_hooks() -> None:
    """Log every uncaught exception from main thread *and* any child thread."""

    def _excepthook(exc_type, exc_value, exc_tb):  # type: ignore[override]
        if issubclass(exc_type, KeyboardInterrupt):
            # Let the default behaviour close the program silently.
            return sys.__excepthook__(exc_type, exc_value, exc_tb)
        logging.critical("UNCAUGHT EXCEPTION", exc_info=(exc_type, exc_value, exc_tb))

    sys.excepthook = _excepthook

    # Python ≥3.8: handle uncaught exceptions inside *any* thread automatically
    def _threading_hook(args: threading.ExceptHookArgs) -> None:  # noqa: D401
        logging.critical(
            "UNCAUGHT EXCEPTION IN THREAD %s", args.thread.name,
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )

    threading.excepthook = _threading_hook


def signal_handler(sig, frame):  # noqa: D401  – signature enforced by signal
    """SIGINT (Ctrl‑C) handler – flush logs then exit fast."""
    logging.warning("[EXIT] Ctrl+C pressed — stopping the bot.")
    logging.shutdown()
    os._exit(0)


def create_file(pid: int, data: str = "0") -> None:
    """Write a small helper‑file used by external monitoring scripts."""
    try:
        temp_path = Path(f"runprocess/temp{pid}.txt")
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path.write_text(data, encoding="utf‑8")
    except Exception:  # noqa: BLE001 – we *want* to log everything here
        logging.exception("create_file failed")


def dynamic_import(module_path: str, class_name: str):
    """Import `class_name` from `module_path` dynamically with full traceback."""
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except Exception:  # noqa: BLE001
        logging.exception("Could not import %s from %s", class_name, module_path)
        sys.exit(1)


def parse_args() -> argparse.Namespace:  # noqa: D401
    parser = argparse.ArgumentParser(description="NSBot Launcher")
    parser.add_argument("game_mode", type=str, help="Game mode to run")
    parser.add_argument("server", type=str, help="Server name")
    parser.add_argument("window_name", type=str, help="Window title")
    parser.add_argument("before_total", type=int, help="Rounds already played")
    parser.add_argument("total", type=int, help="Total rounds to target")
    parser.add_argument("bondling_mode", type=str)
    parser.add_argument("pact_settings", type=str)
    parser.add_argument("crystal_use", type=str)
    parser.add_argument("tomb", type=str)
    parser.add_argument("snowball", type=str)
    parser.add_argument("azure", type=str)
    parser.add_argument("kuro", type=str)
    return parser.parse_args()


# Game mode mapping lives at module level so it is evaluated only once.
GAME_MODES: dict[str, tuple[str, str]] = {
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


# --------------------------------------------------------------------------- #
#                                Main entry                                   #
# --------------------------------------------------------------------------- #

def main() -> None:
    # 1) Init logging first
    MyLog.init(loglv=config["VALUE"]["LOG_LV"])

    # 2) Hook global exceptions **after** logging config is ready
    setup_global_exception_hooks()

    # 3) Signal handling (Ctrl‑C)
    signal.signal(signal.SIGINT, signal_handler)

    # 4) Parse CLI args
    args = parse_args()
    pid = os.getpid()

    logging.debug(
        "HWID: [%s], GameMode: [%s], Server: [%s], Total Rounds: [%s]",
        args.window_name,
        args.game_mode,
        args.server,
        args.total,
    )

    if args.game_mode not in GAME_MODES:
        logging.error("Invalid game mode: %s", args.game_mode)
        sys.exit(1)

    module_path, class_name = GAME_MODES[args.game_mode]
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
    )

    # 5) Run the game mode (can be thread or process depending on implementation)
    try:
        instance.start()

        # keep this thread alive to capture SIGINT while child thread works
        while instance.is_alive():
            instance.join(0.1)

    except KeyboardInterrupt:
        # Redundant – signal_handler will fire – but best keep it for safety.
        logging.warning("[EXIT] Ctrl+C pressed — stopping the bot.")
        logging.shutdown()
        os._exit(0)


if __name__ == "__main__":
    main()
