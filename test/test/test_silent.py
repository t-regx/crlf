from pytest import mark

from test.fixture.application import Application
from test.fixture.directory import directory
from test.fixture.usage import error

arguments = ['-s', '--silent']


@mark.parametrize("argument", arguments)
def test_silent_reline_file(application: Application, argument: str):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', argument, 'file.txt'])
        # then
        assert output.text == ""


def test_silent_reline_file_abs(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--silent', dir('file.txt')])
        # then
        assert output.text == ""


def test_silent_reline_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--silent', 'directory'])
        # then
        assert output.text == ""


def test_silent_reline_directory_abs(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--silent', dir('directory')])
        # then
        assert output.text == ""


def test_silent_ignore_file(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "file\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--silent', 'file.txt'])
    # then
    assert output.text == ""


def test_silent_ignore_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "file\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--silent', 'directory'])
    # then
    assert output.text == ""


def test_silent_malformed(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', b'\x1f\x7f\xee')
        # when
        output = application.run(dir(), ['--to', 'lf', '--silent', 'file.txt'])
    # then
    assert output.output_text == ""


def test_silent_output_error(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', '--silent', 'missing file.txt'])
        # then
        assert output.error == error("file does not exist 'missing file.txt'")
