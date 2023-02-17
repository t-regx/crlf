from pytest import mark

from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.pathseparator import PathSeparator, unix


@mark.skipif(unix, reason='skipping backslash path test on unix')
def test_crlf_backslash(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['directory/file.txt'])
    # then
    assert output.output_text == r"Updated: directory\file.txt" + "\n"


def test_crlf_output_system_separator(application: Application, separator: PathSeparator):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['directory/file.txt'])
    # then
    if separator.forward:
        assert output.output_text == "Updated: directory/file.txt\n"
    else:
        assert output.output_text == "Updated: directory\\file.txt\n"


def test_ignore_output_system_separator(application: Application, separator: PathSeparator):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', b'\x1f\x7f\xee')
        # when
        output = application.run(dir(), ['directory/file.txt'])
    # then
    if separator.forward:
        assert output.output_text == """Failed:  directory/file.txt
         ^ ! expected unicode encoding, malformed encoding found
"""
    else:
        assert output.output_text == r"""Failed:  directory\file.txt
         ^ ! expected unicode encoding, malformed encoding found
"""


def test_crlf_output_system_separator_missing(application: Application, separator: PathSeparator):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['directory/missing.txt'])
    # then
    if separator.forward:
        assert output.output_error == """usage: crlf [-h] [-V] [-q] [-R] filename
crlf: error: file does not exist 'directory/missing.txt'
"""
    else:
        assert output.output_error == r"""usage: crlf [-h] [-V] [-q] [-R] filename
crlf: error: file does not exist 'directory\missing.txt'
"""
