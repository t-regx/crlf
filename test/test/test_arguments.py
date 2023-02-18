from pytest import mark

from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import error


def test_fail_for_unrecognized_option(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', '--invalid', 'foo'])
    # then
    assert output.error == error('unrecognized arguments: --invalid')


def test_fail_for_unrecognized_switch(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', '-X', 'foo'])
    # then
    assert output.error == error('unrecognized arguments: -X')


def test_fail_for_superfluous_argument(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', 'first', 'superfluous'])
    # then
    assert output.error == error('unrecognized arguments: superfluous')


def test_fail_missing_destination(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['first'])
    # then
    assert output.error == error('the following arguments are required: --to')


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
