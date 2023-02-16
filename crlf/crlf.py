from argparse import ArgumentParser
from os import walk
from os.path import isfile, join, isdir, normpath
from typing import Iterator


def main(base: str, arguments: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.add_argument('filename', help='file or directory')
    parser.add_argument('-R', help='recurse into nested directories', action='store_true')
    args = parser.parse_args(arguments)
    convert(parser, base, args.filename)


def convert(parser, base: str, path: str) -> None:
    if path == '':
        parser.error(f"file does not exist '{path}'")
    convert_file_or_directory(parser, base, path)


def convert_file_or_directory(parser, base: str, path: str) -> None:
    absolute_path = join(base, path)
    if isdir(absolute_path):
        convert_directory(base, path)
    elif isfile(absolute_path):
        convert_unicode_file(base, path)
    else:
        parser.error(f"file does not exist '{path}'")


def convert_directory(base: str, path: str) -> None:
    for filename in directory_files(base, path):
        convert_unicode_file(base, filename)


def directory_files(base: str, path: str) -> Iterator[str]:
    _, _, filenames = next(walk(join(base, path)))
    for filename in filenames:
        yield join(path, filename)


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
