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
