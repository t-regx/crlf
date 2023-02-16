from platform import system


def backslash_separator(system: str) -> bool:
    backslash_systems = {
        'Linux': False,
        'Darwin': False,
        'Windows': True
    }
    return backslash_systems[system]


class PathSeparator:
    def __init__(self, unix: bool):
        self._unix = unix

    @property
    def forward(self) -> bool:
        return self._unix

    @property
    def backward(self) -> bool:
        return not self._unix


unix = not backslash_separator(system())
path_separator = PathSeparator(unix)
