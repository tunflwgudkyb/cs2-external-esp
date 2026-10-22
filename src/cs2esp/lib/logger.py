from __future__ import annotations

import logging
import sys

from colorama import Fore, Style, init as colorama_init

colorama_init()

_COLORS = {
    "debug": Fore.CYAN,
    "info": Fore.GREEN,
    "warning": Fore.YELLOW,
    "error": Fore.RED,
}


class _ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        color = _COLORS.get(record.levelname.lower(), "")
        msg = super().format(record)
        return f"{color}{msg}{Style.RESET_ALL}"


def get_logger(level: str = "info") -> logging.Logger:
    log = logging.getLogger("cs2esp")
    if log.handlers:
        return log
    log.setLevel(level.upper())
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(_ColorFormatter("[%(asctime)s] [%(levelname)s] %(message)s",
                                   "%H:%M:%S"))
    log.addHandler(h)
    return log