from argparse import ArgumentParser


def main(arguments: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.add_argument('filename', help='file or directory')
    args = parser.parse_args(arguments)
    parser.error(f"file does not exist '{args.filename}'")
