from argparse import ArgumentParser
from os.path import exists, normpath

from crlf import __version__, __name__
from crlf.fs import RootPath
from crlf.summary import Info, StandardInfo, QuietInfo, SilentInfo


def parsed_arguments(base: str) -> tuple[RootPath, bool, Info, str, bool]:
    parser = ArgumentParser(
        prog=__name__,
        description='Tool to change line endings of text files',
        add_help=False,
        allow_abbrev=False)
    parser.add_argument('filename', help='path to a file or directory')
    parser.add_argument('-h', '--help', help='show this help message', action='help')
    parser.add_argument('-V', '--version', help='show version', action='version', version=__version__)
    quiet = parser.add_mutually_exclusive_group()
    quiet.add_argument('-q', '--quiet',
                       help='change line endings without batch output, only summary', action='store_true')
    quiet.add_argument('-s', '--silent', help='change line endings without any output', action='store_true')
    parser.add_argument('-d', '--dry-run', help='do not actually modify files', action='store_true')
    parser.add_argument('-R', help='recurse into nested directories', dest='recurse', action='store_true')
    parser.add_argument('--to', choices=['crlf', 'lf'], required=True,
                        help='change line endings to CRLF or LF', dest='destination')
    args = parser.parse_args()
    if args.filename == '':
        parser.error(f"file does not exist '{args.filename}'")
    if not exists(args.filename):
        parser.error(f"file does not exist '{normpath(args.filename)}'")
    root = RootPath(base, args.filename)
    return root, args.recurse, info(args.quiet, args.silent), args.destination, args.dry_run


def info(quiet: bool, silent: bool) -> Info:
    if quiet:
        return QuietInfo()
    if silent:
        return SilentInfo()
    return StandardInfo()
