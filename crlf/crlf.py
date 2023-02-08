from argparse import ArgumentParser
from os.path import isfile, join


def main(base: str, arguments: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.add_argument('filename', help='file or directory')
    args = parser.parse_args(arguments)
    convert(parser, base, args.filename)


def convert(parser, base: str, filename: str) -> None:
    absolute_path = join(base, filename)
    if isfile(absolute_path):
        correct_file(absolute_path)
        print(f'Corrected file {filename}')
    else:
        parser.error(f"file does not exist '{filename}'")


def correct_file(filename: str) -> None:
    with open(filename, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        replace = str(lines, 'utf-8').replace("\r", "")
        file.write(bytes(replace, 'utf-8'))
        file.truncate()
