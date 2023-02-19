import os
from os.path import join
from re import sub
from typing import Iterator

from crlf.arguments import parsed_arguments
from crlf.directory import Directory, File
from crlf.summary import Info


def main(base: str, arguments: list[str], width: int) -> None:
    filename, recurse, info, destination, dryrun = parsed_arguments(base, arguments, width)
    reline(Directory(base, filename), recurse, info, destination, dryrun)
    info.summary(dryrun)


def reline(d: Directory, recurse: bool, info: Info, destination: str, dryrun: bool):
    if d.isdir():
        reline_directory(d, recurse, info, destination, dryrun)
    elif d.isfile():
        reline_file(d.file(), info, destination, dryrun)


def reline_directory(d: Directory,
                     recurse: bool,
                     info: Info,
                     destination: str,
                     dryrun: bool) -> None:
    for nested_directory, _, filenames in walk(d, recurse):
        for filename in filenames:
            new_path = join(nested_directory, filename)
            reline_file(d.reset_relative(new_path), info, destination, dryrun)


def walk(d: Directory, recurse: bool) -> Iterator:
    if recurse:
        return os.walk(d.abs())
    return [next(os.walk(d.abs()))]


def reline_file(f: File, info: Info, destination: str, dryrun: bool) -> None:
    with open(f.abs(), 'rb+') as file:
        lines = file.read()
        file.seek(0)
        try:
            content = str(lines, 'utf-8')
        except UnicodeDecodeError:
            info.malformed_encoding(f.without_base())
            return
        replaced = reline_string(destination, content)
        if replaced == content:
            info.already_relined(f.without_base(), destination)
        else:
            if not dryrun:
                file.write(bytes(replaced, 'utf-8'))
                file.truncate()
            info.updated(f.without_base())


def reline_string(direction: str, string: str) -> str:
    return sub(r'\r\n|\r|\n', '\r\n' if direction == 'crlf' else "\n", string)
