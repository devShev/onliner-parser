from enum import Enum


class Font(str, Enum):
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'

    WARN = f'{RED}{BOLD}[WARNING]{NORMAL}{RED}'
    ERROR = f'{RED}{BOLD}[ERROR]{NORMAL}{RED}'
    INFO = f'{GREEN}{BOLD}[INFO]{NORMAL}{GREEN}'
