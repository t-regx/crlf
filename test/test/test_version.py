from test.conftest import Application
from test.fixture.directory import directory


def test_version_option(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--version'])
    # then
    assert output.text == "1.0.0\n"


def test_version_switch(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['-V'])
    # then
    assert output.text == "1.0.0\n"


def test_disallow_abbreviation(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--ver'])
    # then
    assert output.error == """usage: crlf [-h] [-V] [-R] filename
crlf: error: the following arguments are required: filename
"""
