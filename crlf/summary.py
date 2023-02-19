from abc import ABC


class Info(ABC):
    def __init__(self):
        self._updated = 0
        self._failed = 0
        self._ignored = 0

    def updated(self, path: str) -> None:
        self._updated += 1

    def non_unicode(self, path: str) -> None:
        self._failed += 1

    def restricted(self, path: str) -> None:
        self._failed += 1

    def already_relined(self, path: str, destination: str) -> None:
        self._ignored += 1

    def summary(self, dryrun: bool) -> None:
        print("Done. " +
              f"Updated: {self._updated} files, " +
              f"ignored: {self._ignored} files, " +
              f"failed to read: {self._failed} files.")
        if dryrun:
            print("Executed in dry mode, no files were actually modified.")


class SilentInfo(Info):
    def summary(self, dryrun: bool) -> None:
        pass


class QuietInfo(Info):
    pass


class StandardInfo(Info):
    def updated(self, path: str) -> None:
        self._updated += 1
        print('Updated: ' + path)

    def non_unicode(self, path: str) -> None:
        self.__failed(path, '! expected text file in unicode encoding, failed to parse file')

    def restricted(self, path: str) -> None:
        self.__failed(path, 'insufficient permissions to open file')

    def already_relined(self, path: str, destination: str) -> None:
        self._ignored += 1
        self.__print('Ignored:', path, f'file already has {destination.upper()} line endings')

    def __failed(self, path: str, message: str) -> None:
        self._failed += 1
        self.__print('Failed:', path, message)

    def __print(self, type: str, path: str, message: str) -> None:
        print(type.ljust(9) + path)
        print(' ' * 9 + '^ ' + message)
