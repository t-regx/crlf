import os
from argparse import ArgumentParser
from os.path import isfile, join, isdir, normpath, isabs
from typing import Iterator


def main(base: str, arguments: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.add_argument('filename', help='file or directory')
    parser.add_argument('-R', help='recurse into nested directories', dest='recurse', action='store_true')
    args = parser.parse_args(arguments)
    if isabs(args.filename):
        convert(parser, '', args.filename, args.recurse)
    else:
        convert(parser, base, args.filename, args.recurse)


def convert(parser, base: str, path: str, recurse: bool):
    if path == '':
        parser.error(f"file does not exist '{path}'")
    convert_file_or_directory(parser, base, path, recurse)


def convert_file_or_directory(parser, base: str, path: str, recurse: bool) -> None:
    absolute_path = join(base, path)
    if isdir(absolute_path):
        convert_directory(base, path, recurse)
    elif isfile(absolute_path):
        convert_unicode_file(base, path)
    else:
        parser.error(f"file does not exist '{path}'")


def convert_directory(base: str, path: str, recurse: bool) -> None:
    for filepath in directory_files(base, path, recurse):
        convert_unicode_file(base, filepath)


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


def convert_unicode_file(base: str, path: str) -> None:
    try:
        correct_file(join(base, path))
        print(f'Corrected file {normpath(path)}')
    except UnicodeDecodeError:
        print(f'Ignoring file {normpath(path)}')


def correct_file(filename: str) -> None:
    with open(filename, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        replace = str(lines, 'utf-8').replace("\r", "")
        file.write(bytes(replace, 'utf-8'))
        file.truncate()
