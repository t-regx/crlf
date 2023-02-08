from pytest import mark

from test.fixture.application import Application


def test_invoked_without_arguments(application: Application):
    # when
    output = application.run([])
    # then
    assert output.error == """usage: crlf [-h] filename
crlf: error: the following arguments are required: filename
"""


@mark.parametrize("argument", ['-h', '--help'])
def test_help(application: Application, argument: str):
    # when
    output = application.run([argument])
    # then
    assert output.text == """usage: crlf [-h] filename

Tool to change line endings of text files

positional arguments:
  filename    file or directory

options:
  -h, --help  show this help message and exit
"""
