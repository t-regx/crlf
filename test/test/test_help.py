from pytest import mark

from test.fixture.application import Application


def test(application: Application):
    # when
    output = application.run([])
    # then
    assert output == ""


@mark.parametrize("argument", ['-h', '--help'])
def test_help(application: Application, argument: str):
    # when
    output = application.run([argument])
    # then
    assert output == """usage: crlf [-h]

Tool to change line endings of text files

options:
  -h, --help  show this help message and exit
"""
