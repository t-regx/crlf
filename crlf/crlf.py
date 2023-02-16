from argparse import ArgumentParser
from os import walk
from os.path import isfile, join, isdir, normpath
from typing import Generator


def main(base: str, arguments: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.add_argument('filename', help='file or directory')
    args = parser.parse_args(arguments)
    convert(parser, base, args.filename)


def convert(parser, base: str, filename: str) -> None:
    if filename == '':
        parser.error(f"file does not exist '{filename}'")
    else:
        convert_file_or_directory(parser, base, filename)


def convert_file_or_directory(parser, base: str, filename: str) -> None:
    absolute_path = join(base, filename)
    if isdir(absolute_path):
        convert_directory(base, directory=filename)
    elif isfile(absolute_path):
        convert_unicode_file(base, filename)
    else:
        parser.error(f"file does not exist '{filename}'")


def convert_directory(base: str, directory: str) -> None:
    for path, filename in directory_files(join(base, directory)):
        convert_unicode_file(base, join(directory, filename))


def convert_unicode_file(base: str, filename: str) -> None:
    name = normpath(filename)
    try:
        correct_file(join(base, filename))
        print(f'Corrected file {name}')
    except UnicodeDecodeError:
        print(f'Ignoring file {name}')


def directory_files(absolute_path: str) -> Generator:
    path, _, filenames = next(walk(absolute_path))
    for filename in filenames:
        yield join(path, filename), filename


def correct_file(filename: str) -> None:
    with open(filename, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        replace = str(lines, 'utf-8').replace("\r", "")
        file.write(bytes(replace, 'utf-8'))
        file.truncate()
