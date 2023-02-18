from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import updated


def test_crlf_absolute_path(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', dir('file.txt')])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == updated([dir('file.txt')])


def test_crlf_absolute_path_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', dir('directory')])
        # then
        assert dir.open('directory/file.txt') == "line\n"
        assert output.text == updated([dir('directory/file.txt')])


def test_crlf_absolute_path_directory_recurse(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '-R', dir('one')])
        # then
        assert dir.open('one/two/file.txt') == "line\n"
        assert output.text == updated([dir('one/two/file.txt')])
