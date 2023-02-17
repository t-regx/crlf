class Output:
    def __init__(self, output: str, error: str):
        self._output = output
        self._error = error

    @property
    def text(self) -> str:
        return self.output_text.replace('\\', '/')

    @property
    def error(self) -> str:
        return self.output_error.replace('\\', '/')

    @property
    def output_text(self) -> str:
        if self._error == '':
            return self._output
        raise Exception("Tried to read standard output, but there was also error output:\n\n" + self._error)

    @property
    def output_error(self) -> str:
        if self._output == '':
            return self._error
        raise Exception("Tried to read error output, but there is also content in the standard output")
