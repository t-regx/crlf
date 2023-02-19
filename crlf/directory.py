from os.path import isdir, isfile, isabs, join, normpath


class File:
    def __init__(self, base: str, filename: str) -> None:
        self._base = base
        self.filename = filename

    def abs(self) -> str:
        if isabs(self.filename):
            base = ''
        else:
            base = self._base
        return join(base, self.filename)

    def without_base(self) -> str:
        return normpath(self.filename)


class Directory:
    def __init__(self, base: str, filename: str) -> None:
        self._base = base
        self.filename = filename

    def isdir(self) -> bool:
        return isdir(self.abs())

    def isfile(self) -> bool:
        return isfile(self.abs())

    def abs(self) -> str:
        if isabs(self.filename):
            base = ''
        else:
            base = self._base
        return join(base, self.filename)

    def reset_relative(self, path: str) -> File:
        return self.reset(self.relative(path))

    def reset(self, path: str) -> File:
        return File(self._base, path)

    def relative(self, absolute_path: str) -> str:
        if isabs(self.filename):
            return absolute_path
        return absolute_path[len(self._base) + 1:]

    def file(self):
        return File(self._base, self.filename)
