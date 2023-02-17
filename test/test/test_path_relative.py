from pytest import mark

from test.conftest import Application
from test.fixture.directory import directory


@mark.parametrize("path", [
    "one/../one/../one/file.txt",
    "one/../one/file.txt",
    "one/./file.txt",
    "one//file.txt"
])
def test_reline_relative_path(application: Application, path: str):
    # given
    with directory() as dir:
        dir.store('one/file.txt', "line\r\n")
        # when
        output = application.run(dir(), [path])
        # then
        assert dir.open('one/file.txt') == "line\n"
        assert output.text == "Corrected file one/file.txt\n"
