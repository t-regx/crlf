import os
from shutil import rmtree
from tempfile import mkdtemp
from typing import Union


def directory(name: str = None):
    return TemporaryDirectory(name)


class TemporaryDirectory:
    def __init__(self, name: str = None) -> None:
        self._name = name

    def __enter__(self):
        self.test_dir = mkdtemp()
        if self._name is not None:
            self.test_dir = os.path.join(self.test_dir, self._name)
            os.mkdir(self.test_dir)
        return Handle(self.test_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        rmtree(self.test_dir)


class Handle:
    def __init__(self, test_dir: str):
        self.test_dir = test_dir

    def store(self, filename: str, content: Union[str, bytes]):
        if type(content) is str:
            self.__store_bytes(filename, bytes(content, 'utf-8'))
        else:
            self.__store_bytes(filename, content)

    def create(self, directory_name: str) -> None:
        os.mkdir(os.path.join(self.test_dir, directory_name))

    def __store_bytes(self, filename: str, bytes_: bytes):
        folder, _ = os.path.split(self.join(filename))
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(self.join(filename), 'wb') as file:
            file.write(bytes_)

    def open(self, filenames: str) -> str:
        with open(self.join(filenames), 'rb') as file:
            return str(file.read(), 'utf-8')

    def open_bytes(self, *filenames: str) -> bytes:
        with open(self.join(*filenames), 'rb') as file:
            return file.read()

    def __call__(self, *args, **kwargs) -> str:
        return self.join(*args)

    def join(self, *filenames: str) -> str:
        return os.path.join(self.test_dir, *filenames).replace('\\', '/')
