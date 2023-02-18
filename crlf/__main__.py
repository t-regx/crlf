from os import getcwd
from shutil import get_terminal_size
from sys import argv

from crlf.reline import main


def start():
    main(getcwd(), argv[1:], width())


def width() -> int:
    return get_terminal_size().columns


if __name__ == '__main__':
    start()
