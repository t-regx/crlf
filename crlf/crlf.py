from argparse import ArgumentParser
from os.path import isfile, join


def main(base: str, arguments: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.add_argument('filename', help='file or directory')
    args = parser.parse_args(arguments)
    convert(parser, base, args.filename)


def convert(parser, base: str, filename: str) -> None:
    if isfile(join(base, filename)):
        print(f'Corrected file {filename}')
    else:
        parser.error(f"file does not exist '{filename}'")
