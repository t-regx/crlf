from pytest import mark

from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import error


def test_fail_for_unrecognized_option(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--invalid', 'foo'])
    # then
    assert output.error == error('unrecognized arguments: --invalid')


def test_fail_for_unrecognized_switch(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['-X', 'foo'])
    # then
    assert output.error == error('unrecognized arguments: -X')


def test_fail_for_superfluous_argument(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['first', 'superfluous'])
    # then
    assert output.error == error('unrecognized arguments: superfluous')


@mark.parametrize('arguments', [
    ['-q', '-s'],
    ['--quiet', '--silent'],
])
def test_fail_quiet_silent(application: Application, arguments: list[str]):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), arguments)
    # then
    assert output.error == error('argument -s/--silent: not allowed with argument -q/--quiet')
