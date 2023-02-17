def error(message: str) -> str:
    return f"""usage: crlf [-h] [-V] [-q] [-R] filename
crlf: error: {message}
"""


def updated(filenames: list[str]) -> str:
    return ''.join([f"Updated: {filename}\n" for filename in filenames])


def malformed(filenames: list[str]) -> str:
    if len(filenames) == 1:
        return _malformed(filenames[0])
    raise


def _malformed(filename: str) -> str:
    return f"""Failed:  {filename}
         ^ ! expected unicode encoding, malformed encoding found
"""


def ignored(filenames: list[str]) -> str:
    return ''.join([_ignored(filename) for filename in filenames])


def _ignored(filename: str) -> str:
    return f"""Ignored: {filename}
         ^ file already has LF line endings
"""
