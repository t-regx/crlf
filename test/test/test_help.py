from pytest import mark

from crlf.crlf import main


def test(capsys):
    # when
    try:
        main([])
    except SystemExit:
        pass
    # then
    assert capsys.readouterr().out == ''


@mark.parametrize("argument", ['-h', '--help'])
def test_help(capsys, argument: str):
    # when
    try:
        main([argument])
    except SystemExit:
        pass
    # then
    assert capsys.readouterr().out == """usage: crlf [-h]

Tool to change line endings of text files

options:
  -h, --help  show this help message and exit
"""
