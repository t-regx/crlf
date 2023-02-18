from pytest import mark

from test.fixture.application import Application
from test.fixture.directory import directory
from test.fixture.usage import error


def test_invoked_without_arguments(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), [])
    # then
    assert output.error == error('the following arguments are required: filename, --to')


@mark.parametrize("argument", ['-h', '--help'])
def test_help(application: Application, argument: str):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), [argument])
    # then
    assert output.text == """usage: crlf [-h] [-V] [-q | -s] [-R] --to {crlf,lf} filename

Tool to change line endings of text files

positional arguments:
  filename        path to a file or directory

options:
  -h, --help      show this help message
  -V, --version   show version
  -q, --quiet     change line endings without batch output, only summary
  -s, --silent    change line endings without any output
  -R              recurse into nested directories
  --to {crlf,lf}  change line endings to CRLF or LF
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
