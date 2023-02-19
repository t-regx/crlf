import os
from os import getcwd
from os.path import join
from re import sub
from typing import Iterator

from crlf.arguments import parsed_arguments
from crlf.fs import Directory, File, RootPath
from crlf.summary import Info


def main() -> None:
    root, recurse, info, destination, dryrun = parsed_arguments(getcwd())
    reline(root, recurse, info, destination, dryrun)
    info.summary(dryrun)


def reline(root: RootPath, recurse: bool, info: Info, destination: str, dryrun: bool):
    if root.isdir():
        reline_directory(root.dir(), recurse, info, destination, dryrun)
    elif root.isfile():
        reline_file(root.file(), info, destination, dryrun)


def reline_directory(dir: Directory, recurse: bool, info: Info, destination: str, dryrun: bool) -> None:
    for file in directory_files(dir, recurse):
        reline_file(file, info, destination, dryrun)


def directory_files(dir: Directory, recurse: bool) -> Iterator[File]:
    for nested_directory, _, filenames in walk(dir, recurse):
        for filename in filenames:
            yield dir.child(join(nested_directory, filename))


def walk(directory: Directory, recurse: bool) -> Iterator:
    if recurse:
        return os.walk(directory.abs)
    return [next(os.walk(directory.abs))]


def reline_file(file: File, info: Info, destination: str, dryrun: bool) -> None:
    try:
        try_reline_file(file, info, destination, dryrun)
    except PermissionError:
        info.restricted(file.relative)
    except UnicodeDecodeError:
        info.non_unicode(file.relative)


def try_reline_file(subject: File, info: Info, destination: str, dryrun: bool) -> None:
    with open(subject.abs, 'rb+') as file:
        lines = file.read()
        file.seek(0)
        content = str(lines, 'utf-8')
        replaced = reline_string(destination, content)
        if replaced == content:
            info.already_relined(subject.relative, destination)
        else:
            if not dryrun:
                file.write(bytes(replaced, 'utf-8'))
                file.truncate()
            info.updated(subject.relative)


def reline_string(direction: str, string: str) -> str:
    return sub(r'\r\n|\r|\n', '\r\n' if direction == 'crlf' else "\n", string)
