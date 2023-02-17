from argparse import ArgumentParser, HelpFormatter
from os.path import exists, join, normpath

from crlf import __version__


def parsed_arguments(base: str, arguments: list[str]) -> tuple[str, bool, bool]:
    parser = ArgumentParser(
        prog='crlf',
        description='Tool to change line endings of text files',
        formatter_class=formatter,
        add_help=False,
        allow_abbrev=False)
    parser.add_argument('filename', help='path to a file or directory')
    parser.add_argument('-h', '--help', help='show this help message', action='help')
    parser.add_argument('-V', '--version', help='show version', action='version', version=__version__)
    parser.add_argument('-q', '--quiet', '--silent', help='change line endings without any output', action='store_true')
    parser.add_argument('-R', help='recurse into nested directories', dest='recurse', action='store_true')
    args = parser.parse_args(arguments)
    if args.filename == '':
        parser.error(f"file does not exist '{args.filename}'")
    if not exists(join(base, args.filename)):
        parser.error(f"file does not exist '{normpath(args.filename)}'")
    return args.filename, args.recurse, args.quiet


def formatter(prog: str) -> HelpFormatter:
    return HelpFormatter(prog, max_help_position=52)
