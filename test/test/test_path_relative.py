from pytest import mark

from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import updated


@mark.parametrize("path", [
    "directory/../directory/../directory/file.txt",
    "directory/../directory/file.txt",
    "directory/./file.txt",
    "directory//file.txt"
])
def test_reline_relative_path(application: Application, path: str):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), [path])
        # then
        assert dir.open('directory/file.txt') == "line\n"
        assert output.text == updated(['directory/file.txt'])
