from os.path import isdir, isfile, isabs, join, normpath


class RootPath:
    def __init__(self, base: str, path: str) -> None:
        self._base = base
        self._path = path

    def isdir(self) -> bool:
        return isdir(join(self._base, self._path))

    def isfile(self) -> bool:
        return isfile(join(self._base, self._path))

    def file(self):
        return File(self._base, self._path)

    def dir(self):
        return Directory(self._base, self._path)


class File:
    def __init__(self, base: str, path: str) -> None:
        self._base = base
        self._path = path

    @property
    def abs(self) -> str:
        return join(self._base, self._path)

    @property
    def relative(self) -> str:
        return normpath(self._path)


class Directory:
    def __init__(self, base: str, filename: str) -> None:
        self._base = base
        self.filename = filename

    @property
    def abs(self) -> str:
        return join(self._base, self.filename)

    def child(self, absolute_path: str) -> File:
        if isabs(self.filename):
            return File(self._base, absolute_path)
        return File(self._base, absolute_path[len(self._base) + 1:])
