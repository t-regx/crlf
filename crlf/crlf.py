import os
from argparse import ArgumentParser
from os.path import isfile, join, isdir, normpath, isabs
from typing import Iterator

from . import __version__


def main(base: str, arguments: list[str]) -> None:
    parser = ArgumentParser(
        prog='crlf',
        description='Tool to change line endings of text files',
        add_help=False,
        allow_abbrev=False)
    parser.add_argument('filename', help='file or directory')
    parser.add_argument('-h', '--help', help='show this help message', action='help')
    parser.add_argument('-V', '--version', help='show version', action='version', version=__version__)
    parser.add_argument('-R', help='recurse into nested directories', dest='recurse', action='store_true')
    args = parser.parse_args(arguments)
    if isabs(args.filename):
        reline(parser, '', args.filename, args.recurse)
    else:
        reline(parser, base, args.filename, args.recurse)


def reline(parser, base: str, path: str, recurse: bool):
    if path == '':
        parser.error(f"file does not exist '{path}'")
    reline_file_or_directory(parser, base, path, recurse)


def reline_file_or_directory(parser, base: str, path: str, recurse: bool) -> None:
    absolute_path = join(base, path)
    if isdir(absolute_path):
        reline_directory(base, path, recurse)
    elif isfile(absolute_path):
        reline_unicode_file(base, path)
    else:
        norm = path.replace('\\', os.sep).replace('/', os.sep)
        parser.error(f"file does not exist '{norm}'")


def reline_directory(base: str, path: str, recurse: bool) -> None:
    for filepath in directory_files(base, path, recurse):
        reline_unicode_file(base, filepath)


def directory_files(base: str, path: str, recurse: bool) -> Iterator[str]:
    for directory, _, filenames in walk(join(base, path), recurse):
        short_path = unjoin(base, directory)
        for filename in filenames:
            yield join(short_path, filename)


def walk(absolute_path: str, recurse: bool) -> Iterator:
    if recurse:
        return os.walk(absolute_path)
    return [next(os.walk(absolute_path))]


def unjoin(base: str, absolute_path: str) -> str:
    if base == '':
        return absolute_path
    return absolute_path[len(base) + 1:]


def reline_unicode_file(base: str, path: str) -> None:
    try:
        correct_file(join(base, path))
        print('Updated: ' + normpath(path))
    except UnicodeDecodeError:
        print('Failed:  ' + normpath(path))
        print('         ^ ! expected unicode encoding, malformed encoding found')


def correct_file(filename: str) -> None:
    with open(filename, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        replace = str(lines, 'utf-8').replace("\r", "")
        file.write(bytes(replace, 'utf-8'))
        file.truncate()
