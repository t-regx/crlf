from argparse import ArgumentParser, HelpFormatter
from os.path import exists, join, normpath

from crlf import __version__, __name__
from crlf.summary import Info, StandardInfo, QuietInfo, SilentInfo


def parsed_arguments(base: str, arguments: list[str], width: int) -> tuple[str, bool, Info, str]:
    parser = ArgumentParser(
        prog=__name__,
        description='Tool to change line endings of text files',
        add_help=False,
        formatter_class=lambda prog: HelpFormatter(prog, width=width-2),
        allow_abbrev=False)
    parser.add_argument('filename', help='path to a file or directory')
    parser.add_argument('-h', '--help', help='show this help message', action='help')
    parser.add_argument('-V', '--version', help='show version', action='version', version=__version__)
    quiet = parser.add_mutually_exclusive_group()
    quiet.add_argument('-q', '--quiet',
                       help='change line endings without batch output, only summary', action='store_true')
    quiet.add_argument('-s', '--silent', help='change line endings without any output', action='store_true')
    parser.add_argument('-R', help='recurse into nested directories', dest='recurse', action='store_true')
    parser.add_argument('--to', choices=['crlf', 'lf'], required=True,
                        help='change line endings to CRLF or LF', dest='destination')
    args = parser.parse_args(arguments)
    if args.filename == '':
        parser.error(f"file does not exist '{args.filename}'")
    if not exists(join(base, args.filename)):
        parser.error(f"file does not exist '{normpath(args.filename)}'")
    return args.filename, args.recurse, info(args.quiet, args.silent), args.destination


def info(quiet: bool, silent: bool) -> Info:
    if quiet:
        return QuietInfo()
    if silent:
        return SilentInfo()
    return StandardInfo()
