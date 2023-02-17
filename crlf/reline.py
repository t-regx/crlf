import os
from os.path import isfile, join, isdir, normpath, isabs
from typing import Iterator

from crlf.arguments import parsed_arguments


def main(base: str, arguments: list[str]) -> None:
    filename, recurse = parsed_arguments(base, arguments)
    if isabs(filename):
        reline('', filename, recurse)
    else:
        reline(base, filename, recurse)


def reline(base: str, path: str, recurse: bool):
    absolute_path = join(base, path)
    if isdir(absolute_path):
        reline_directory(base, path, recurse)
    elif isfile(absolute_path):
        reline_file(base, path)


def reline_directory(base: str, path: str, recurse: bool) -> None:
    for filepath in directory_files(base, path, recurse):
        reline_file(base, filepath)


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


def reline_file(base: str, path: str) -> None:
    filename = join(base, path)
    with open(filename, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        try:
            content = str(lines, 'utf-8')
        except UnicodeDecodeError:
            notify_malformed_encoding(path)
            return
        replace = content.replace("\r", "")
        if replace == content:
            notify_already_relined(path)
        else:
            file.write(bytes(replace, 'utf-8'))
            file.truncate()
            notify_updated(path)


def notify_updated(path: str) -> None:
    print('Updated: ' + normpath(path))


def notify_malformed_encoding(path: str) -> None:
    print('Failed:  ' + normpath(path))
    print('         ^ ! expected unicode encoding, malformed encoding found')


def notify_already_relined(path: str) -> None:
    print('Ignored: ' + normpath(path))
    print('         ^ file already has LF line endings')
