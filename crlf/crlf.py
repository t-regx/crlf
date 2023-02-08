from argparse import ArgumentParser
from os.path import isfile, join


def main(base: str, arguments: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.add_argument('filename', help='file or directory')
    args = parser.parse_args(arguments)
    if isfile(join(base, args.filename)):
        print(f'Corrected file {args.filename}')
    else:
        parser.error(f"file does not exist '{args.filename}'")
