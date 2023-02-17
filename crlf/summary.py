from abc import abstractmethod, ABC


class Info(ABC):
    @abstractmethod
    def updated(self, path: str) -> None:
        pass

    @abstractmethod
    def malformed_encoding(self, path: str) -> None:
        pass

    @abstractmethod
    def already_relined(self, path: str) -> None:
        pass

    @abstractmethod
    def summary(self) -> None:
        pass


class QuietInfo(Info):
    def updated(self, path: str) -> None:
        pass

    def malformed_encoding(self, path: str) -> None:
        pass

    def already_relined(self, path: str) -> None:
        pass

    def summary(self) -> None:
        pass


class PrintInfo(Info):
    def __init__(self):
        self._updated = 0
        self._malformed = 0
        self._ignored = 0

    def updated(self, path: str) -> None:
        self._updated += 1
        print('Updated: ' + path)

    def malformed_encoding(self, path: str) -> None:
        self._malformed += 1
        print('Failed:  ' + path)
        print('         ^ ! expected unicode encoding, malformed encoding found')

    def already_relined(self, path: str) -> None:
        self._ignored += 1
        print('Ignored: ' + path)
        print('         ^ file already has LF line endings')

    def summary(self) -> None:
        print("Done. " +
              f"Updated: {self._updated} files, " +
              f"ignored: {self._ignored} files, " +
              f"and encountered malformed: {self._malformed} files.")
