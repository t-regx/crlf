import os
from os.path import isfile, join, isdir, normpath, isabs
from re import sub
from typing import Iterator

from crlf.arguments import parsed_arguments
from crlf.summary import Info


def main(base: str, arguments: list[str]) -> None:
    filename, recurse, info, destination = parsed_arguments(base, arguments)
    if isabs(filename):
        reline('', filename, recurse, info, destination)
    else:
        reline(base, filename, recurse, info, destination)
    info.summary()


def reline(base: str, path: str, recurse: bool, info: Info, destination: str):
    absolute_path = join(base, path)
    if isdir(absolute_path):
        reline_directory(base, path, recurse, info, destination)
    elif isfile(absolute_path):
        reline_file(base, path, info, destination)


def reline_directory(base: str, path: str, recurse: bool, info: Info, destination: str) -> None:
    for filepath in directory_files(base, path, recurse):
        reline_file(base, filepath, info, destination)


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


def reline_file(base: str, path: str, info: Info, destination: str) -> None:
    filename = join(base, path)
    with open(filename, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        try:
            content = str(lines, 'utf-8')
        except UnicodeDecodeError:
            info.malformed_encoding(normpath(path))
            return
        replaced = reline_string(destination, content)
        if replaced == content:
            info.already_relined(normpath(path), destination)
        else:
            file.write(bytes(replaced, 'utf-8'))
            file.truncate()
            info.updated(normpath(path))


def reline_string(direction: str, string: str) -> str:
    if direction == 'crlf':
        return sub(r'(?<!\r)\n', '\r\n', string)
    return string.replace("\r\n", "\n")
