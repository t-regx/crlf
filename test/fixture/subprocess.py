from os import environ, path
from subprocess import run, CompletedProcess
from sys import executable

import crlf


def completed_process(arguments: list[str]) -> CompletedProcess:
    try:
        return run(
            env=dict(environ, PYTHONPATH=project_path()),
            args=[executable, '-m', crlf.__name__, *arguments],
            capture_output=True)
    except OSError:
        raise Exception("Failed to spawn sub-process") from None


def project_path() -> str:
    return path.dirname(path.dirname(crlf.__file__))
