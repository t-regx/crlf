from pytest import mark

from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.pathseparator import PathSeparator, unix
from test.fixture.usage import malformed, error, updated


@mark.skipif(unix, reason='skipping backslash path test on unix')
def test_crlf_backslash(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['directory/file.txt'])
    # then
    assert output.output_text == updated([r"directory\file.txt"])


def test_crlf_output_system_separator(application: Application, separator: PathSeparator):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['directory/file.txt'])
    # then
    if separator.forward:
        assert output.output_text == updated(['directory/file.txt'])
    else:
        assert output.output_text == updated([r'directory\file.txt'])


def test_ignore_output_system_separator(application: Application, separator: PathSeparator):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', b'\x1f\x7f\xee')
        # when
        output = application.run(dir(), ['directory/file.txt'])
    # then
    if separator.forward:
        assert output.output_text == malformed(['directory/file.txt'])
    else:
        assert output.output_text == malformed([r'directory\file.txt'])


def test_crlf_output_system_separator_missing(application: Application, separator: PathSeparator):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['directory/missing.txt'])
    # then
    if separator.forward:
        assert output.output_error == error("file does not exist 'directory/missing.txt'")
    else:
        assert output.output_error == error(r"file does not exist 'directory\missing.txt'")
