from pytest import mark

from test.fixture.application import Application
from test.fixture.directory import directory
from test.fixture.usage import error, summary

arguments = ['-q', '--quiet']


@mark.parametrize("argument", arguments)
def test_quiet_reline_file(application: Application, argument: str):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', argument, 'file.txt'])
        # then
        assert output.text == summary(1)


def test_quiet_reline_file_abs(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--quiet', dir('file.txt')])
        # then
        assert output.text == summary(1)


def test_quiet_reline_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--quiet', 'directory'])
        # then
        assert output.text == summary(1)


def test_quiet_reline_directory_abs(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--quiet', dir('directory')])
        # then
        assert output.text == summary(1)


@mark.parametrize("argument", arguments)
def test_quiet_ignore_file(application: Application, argument: str):
    # given
    with directory() as dir:
        dir.store('file.txt', "file\n")
        # when
        output = application.run(dir(), ['--to', 'lf', argument, 'file.txt'])
    # then
    assert output.text == summary(ignored=1)


def test_quiet_ignore_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', "file\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '--quiet', 'directory'])
    # then
    assert output.text == summary(ignored=1)


@mark.parametrize("argument", arguments)
def test_quiet_malformed(application: Application, argument: str):
    # given
    with directory() as dir:
        dir.store('file.txt', b'\x1f\x7f\xee')
        # when
        output = application.run(dir(), ['--to', 'lf', argument, 'file.txt'])
    # then
    assert output.output_text == summary(malformed=1)


@mark.parametrize("argument", arguments)
def test_quiet_output_error(application: Application, argument: str):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', argument, 'missing file.txt'])
        # then
        assert output.error == error("file does not exist 'missing file.txt'")
