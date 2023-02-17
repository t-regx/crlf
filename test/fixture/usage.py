def error(message: str) -> str:
    return f"""usage: crlf [-h] [-V] [-q | -s] [-R] filename
crlf: error: {message}
"""


def summary(updated: int = 0, ignored: int = 0, malformed: int = 0) -> str:
    return f'Done. Updated: {updated} files, ignored: {ignored} files, and encountered malformed: {malformed} files.\n'


def updated(filenames: list[str]) -> str:
    return ''.join([f"Updated: {filename}\n" for filename in filenames]) + summary(updated=len(filenames))


def ignored(filenames: list[str]) -> str:
    return ''.join([_ignored(filename) for filename in filenames]) + summary(ignored=len(filenames))


def malformed(filenames: list[str]) -> str:
    return ''.join([_malformed(filename) for filename in filenames]) + summary(malformed=len(filenames))


def _ignored(filename: str) -> str:
    return f"""Ignored: {filename}
         ^ file already has LF line endings
"""


def _malformed(filename: str) -> str:
    return f"""Failed:  {filename}
         ^ ! expected unicode encoding, malformed encoding found
"""
