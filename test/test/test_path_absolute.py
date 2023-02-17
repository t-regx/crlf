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


def test_crlf_absolute_path_directory_recurse(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['-R', dir('one')])
        # then
        assert dir.open('one/two/file.txt') == "line\n"
        assert output.text == f"Corrected file {dir('one/two/file.txt')}\n"
