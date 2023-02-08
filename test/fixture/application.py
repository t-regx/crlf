import sys
from abc import abstractmethod, ABC
from io import StringIO

from crlf.crlf import main
from test.fixture.subprocess import completed_process


class Application(ABC):
    @abstractmethod
    def run(self, arguments: list[str]) -> str:
        pass


class ProcessApplication(Application):
    def run(self, arguments: list[str]) -> str:
        result = completed_process(arguments)
        return self.string(result.stdout)

    def string(self, output: bytes) -> str:
        return str(output, 'utf-8').replace('\r\n', '\n')


class MemoryApplication(Application):
    def run(self, arguments: list[str]) -> str:
        _sys_stdout = sys.stdout
        sys.stdout = LinesStringIO()
        try:
            main(arguments)
            return str(sys.stdout)
        except SystemExit:
            return str(sys.stdout)
        finally:
            sys.stdout = _sys_stdout


class LinesStringIO(StringIO):
    def __init__(self):
        super().__init__()
        self._lines = []

    def write(self, s: str) -> int:
        self._lines.append(s)
        return super().write(s)

    def __str__(self) -> str:
        return ''.join(self._lines)
