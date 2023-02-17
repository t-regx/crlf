from pytest import mark

from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.pathseparator import PathSeparator, unix


@mark.skipif(unix, reason='skipping backslash path test on unix')
def test_crlf_backslash(application: Application):
    # given
    with directory() as dir:
        dir.store('one/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['one/file.txt'])
    # then
    assert output.output == r"Updated: one\file.txt" + "\n"


def test_crlf_log_output_system_separator(application: Application, separator: PathSeparator):
    # given
    with directory() as dir:
        dir.store('one/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['one/file.txt'])
    # then
    if separator.forward:
        assert output.output == "Updated: one/file.txt\n"
    else:
        assert output.output == "Updated: one\\file.txt\n"


def test_ignore_log_output_system_separator(application: Application, separator: PathSeparator):
    # given
    with directory() as dir:
        dir.store('one/file.txt', b'\x1f\x7f\xee')
        # when
        output = application.run(dir(), ['one/file.txt'])
    # then
    if separator.forward:
        assert output.output == """Failed:  one/file.txt
         ^ ! expected unicode encoding, malformed encoding found
"""
    else:
        assert output.output == r"""Failed:  one\file.txt
         ^ ! expected unicode encoding, malformed encoding found
"""
