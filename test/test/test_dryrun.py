from pytest import mark

from test.fixture.application import Application
from test.fixture.directory import directory
from test.fixture.usage import summary, updated, ignored, failed, restricted


@mark.parametrize("argument", ['-d', '--dry-run'])
def test_dryrun(application: Application, argument: str):
    # given
    with directory() as dir:
        dir.store('file.txt', 'line\r\n')
        # when
        output = application.run(dir(), ['--to', 'lf', argument, 'file.txt'])
        # then
        assert dir.open('file.txt') == 'line\r\n'
        assert output.text == updated(['file.txt'], dryrun=True)


def test_dryrun_ignored(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', 'line\n')
        # when
        output = application.run(dir(), ['--to', 'lf', '--dry-run', 'file.txt'])
        # then
        assert dir.open('file.txt') == 'line\n'
        assert output.text == ignored(['file.txt'], 'lf', dryrun=True)


def test_dryrun_failed(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', b'line\r\n \x1f\x7f\xee \x0d\x0a')
        # when
        output = application.run(dir(), ['--to', 'lf', '--dry-run', 'file.txt'])
        # then
        assert dir.open_bytes('file.txt') == b'line\r\n \x1f\x7f\xee \x0d\x0a'
        assert output.text == failed(['file.txt'], dryrun=True)


@mark.parametrize("argument", ['-d', '--dry-run'])
def test_dryrun_directory(application: Application, argument: str):
    # given
    with directory() as dir:
        dir.store('directory/file.txt', 'line\r\n')
        # when
        output = application.run(dir(), ['--to', 'lf', argument, 'directory'])
        # then
        assert dir.open('directory/file.txt') == 'line\r\n'
        assert output.text == updated(['directory/file.txt'], dryrun=True)


def test_dryrun_absolute_path(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', 'line\r\n')
        # when
        output = application.run(dir(), ['--to', 'lf', '--dry-run', dir('file.txt')])
        # then
        assert dir.open(dir('file.txt')) == 'line\r\n'
        assert output.text == updated([dir('file.txt')], dryrun=True)


def test_dryrun_summary(application: Application):
    # given
    with directory() as dir:
        dir.create('directory')
        # when
        output = application.run(dir(), ['--to', 'lf', '--dry-run', 'directory'])
    # then
    assert output.text == summary(dryrun=True)


def test_dryrun_summary_quiet(application: Application):
    # given
    with directory() as dir:
        dir.create('directory')
        # when
        output = application.run(dir(), ['--to', 'lf', '--dry-run', '--quiet', 'directory'])
    # then
    assert output.text == summary(dryrun=True)


def test_dryrun_summary_silent(application: Application):
    # given
    with directory() as dir:
        dir.create('directory')
        # when
        output = application.run(dir(), ['--to', 'lf', '--dry-run', '--silent', 'directory'])
    # then
    assert output.text == ''


def test_failed_restricted_file(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', 'line\n')
        with dir.permissions(['file.txt'], 0):
            # when
            output = application.run(dir(), ['--to', 'lf', '--dry-run', 'file.txt'])
        # then
        assert output.text == restricted(['file.txt'], dryrun=True)
