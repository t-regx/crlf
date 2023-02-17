from abc import ABC


class Info(ABC):
    def __init__(self):
        self._updated = 0
        self._malformed = 0
        self._ignored = 0

    def updated(self, path: str) -> None:
        self._updated += 1

    def malformed_encoding(self, path: str) -> None:
        self._malformed += 1

    def already_relined(self, path: str, destination: str) -> None:
        self._ignored += 1

    def summary(self) -> None:
        print("Done. " +
              f"Updated: {self._updated} files, " +
              f"ignored: {self._ignored} files, " +
              f"and encountered malformed: {self._malformed} files.")


class SilentInfo(Info):
    def summary(self) -> None:
        pass


class QuietInfo(Info):
    pass


class StandardInfo(Info):
    def updated(self, path: str) -> None:
        self._updated += 1
        print('Updated: ' + path)

    def malformed_encoding(self, path: str) -> None:
        self._malformed += 1
        print('Failed:  ' + path)
        print('         ^ ! expected unicode encoding, malformed encoding found')

    def already_relined(self, path: str, destination: str) -> None:
        self._ignored += 1
        print(f'Ignored: {path}')
        print(f'         ^ file already has {destination.upper()} line endings')
