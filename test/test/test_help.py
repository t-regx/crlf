from pytest import mark

from test.fixture.application import Application
from test.fixture.directory import directory


def test_invoked_without_arguments(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), [])
    # then
    assert output.error == """usage: crlf [-h] [-R] filename
crlf: error: the following arguments are required: filename
"""


@mark.parametrize("argument", ['-h', '--help'])
def test_help(application: Application, argument: str):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), [argument])
    # then
    assert output.text == """usage: crlf [-h] [-R] filename

Tool to change line endings of text files

positional arguments:
  filename    file or directory

options:
  -h, --help  show this help message and exit
  -R          recurse into nested directories
"""


@mark.parametrize("argument", ['-h', '--help'])
def test_help_does_not_modify_files(application: Application, argument: str):
    # given
    with directory() as dir:
        dir.store('file.txt', 'line\r\n')
        # when
        application.run(dir(), [argument])
        # then
        assert dir.open('file.txt') == 'line\r\n'
