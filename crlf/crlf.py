from argparse import ArgumentParser
from os.path import isfile, join


def main(base: str, arguments: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.add_argument('filename', help='file or directory')
    args = parser.parse_args(arguments)
    convert(parser, join(base, args.filename), args.filename)


def convert(parser, absolute_path: str, filename: str) -> None:
    if isfile(absolute_path):
        convert_unicode_file(absolute_path, filename)
    else:
        parser.error(f"file does not exist '{filename}'")


def convert_unicode_file(absolute_path: str, filename: str) -> None:
    try:
        correct_file(absolute_path)
        print(f'Corrected file {filename}')
    except UnicodeDecodeError:
        print(f'Ignoring file {filename}')


def correct_file(filename: str) -> None:
    with open(filename, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        replace = str(lines, 'utf-8').replace("\r", "")
        file.write(bytes(replace, 'utf-8'))
        file.truncate()
