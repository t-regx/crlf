from test.conftest import Application
from test.fixture.directory import directory


def test_crlf_absolute_path(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), [dir('file.txt')])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == f"Corrected file {dir('file.txt')}\n"


def test_crlf_absolute_path_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/file.txt', "line\r\n")
        # when
        output = application.run(dir(), [dir('one')])
        # then
        assert dir.open('one/file.txt') == "line\n"
        assert output.text == f"Corrected file {dir('one/file.txt')}\n"
