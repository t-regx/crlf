from argparse import ArgumentParser


def main(args: list[str]) -> None:
    parser = ArgumentParser('crlf', description='Tool to change line endings of text files')
    parser.parse_args(args)
