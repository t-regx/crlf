import os
from os.path import isfile, join, isdir, normpath, isabs
from typing import Iterator

from crlf.arguments import parsed_arguments
from crlf.summary import Info


def main(base: str, arguments: list[str]) -> None:
    filename, recurse, info = parsed_arguments(base, arguments)
    if isabs(filename):
        reline('', filename, recurse, info)
    else:
        reline(base, filename, recurse, info)
    info.summary()


def reline(base: str, path: str, recurse: bool, info: Info):
    absolute_path = join(base, path)
    if isdir(absolute_path):
        reline_directory(base, path, recurse, info)
    elif isfile(absolute_path):
        reline_file(base, path, info)


def reline_directory(base: str, path: str, recurse: bool, info: Info) -> None:
    for filepath in directory_files(base, path, recurse):
        reline_file(base, filepath, info)


def directory_files(base: str, path: str, recurse: bool) -> Iterator[str]:
    for directory, _, filenames in walk(join(base, path), recurse):
        short_path = unjoin(base, directory)
        for filename in filenames:
            yield join(short_path, filename)


def walk(absolute_path: str, recurse: bool) -> Iterator:
    if recurse:
        return os.walk(absolute_path)
    return [next(os.walk(absolute_path))]


def unjoin(base: str, absolute_path: str) -> str:
    if base == '':
        return absolute_path
    return absolute_path[len(base) + 1:]


def reline_file(base: str, path: str, info: Info) -> None:
    filename = join(base, path)
    with open(filename, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        try:
            content = str(lines, 'utf-8')
        except UnicodeDecodeError:
            info.malformed_encoding(normpath(path))
            return
        replace = content.replace("\r", "")
        if replace == content:
            info.already_relined(normpath(path), 'lf')
        else:
            file.write(bytes(replace, 'utf-8'))
            file.truncate()
            info.updated(normpath(path))
