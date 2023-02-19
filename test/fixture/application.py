import os
import sys
from abc import abstractmethod, ABC
from io import StringIO
from os import chdir, environ
from os.path import dirname

from test.fixture.output import Output
from test.fixture.subprocess import completed_process


class Application(ABC):
    @abstractmethod
    def run(self, directory: str, arguments: list[str], width: int = 80) -> Output:
        pass


class ProcessApplication(Application):
    def run(self, directory: str, arguments: list[str], width: int = 80) -> Output:
        result = completed_process(directory, arguments, width)
        return Output(self.string(result.stdout), self.string(result.stderr))

    def string(self, output: bytes) -> str:
        return str(output, 'utf-8').replace('\r\n', '\n')


class MemoryApplication(Application):
    def run(self, directory: str, arguments: list[str], width: int = 80) -> Output:
        _sys_stdout = sys.stdout
        _sys_stderr = sys.stderr
        sys.stdout = LinesStringIO()
        sys.stderr = LinesStringIO()
        self.execute(directory, arguments, width)
        try:
            return Output(str(sys.stdout), str(sys.stderr))
        finally:
            sys.stdout = _sys_stdout
            sys.stderr = _sys_stderr

    def execute(self, directory: str, arguments: list[str], width: int) -> None:
        chdir(directory)
        sys.argv = ['', *arguments]
        environ['COLUMNS'] = str(width)
        from crlf.__main__ import main
        try:
            main()
        except SystemExit:
            pass
        os.chdir(dirname(dirname(directory)))


class LinesStringIO(StringIO):
    def __init__(self):
        super().__init__()
        self._lines = []

    def write(self, s: str) -> int:
        self._lines.append(s)
        return super().write(s)

    def __str__(self) -> str:
        return ''.join(self._lines)
