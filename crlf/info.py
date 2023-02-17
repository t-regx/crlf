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


class QuietInfo(Info):
    def updated(self, path: str) -> None:
        pass

    def malformed_encoding(self, path: str) -> None:
        pass

    def already_relined(self, path: str) -> None:
        pass


class PrintInfo(Info):
    def updated(self, path: str) -> None:
        print('Updated: ' + path)

    def malformed_encoding(self, path: str) -> None:
        print('Failed:  ' + path)
        print('         ^ ! expected unicode encoding, malformed encoding found')

    def already_relined(self, path: str) -> None:
        print('Ignored: ' + path)
        print('         ^ file already has LF line endings')
