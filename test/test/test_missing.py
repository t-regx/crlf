from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.pytest.mark import memoryonly
from test.fixture.usage import error


@memoryonly
def test_invoked_with_empty_filename(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', ''])
    # then
    assert output.error == error("file does not exist ''")


def test_invoked_with_missing_file(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', 'missing.txt'])
    # then
    assert output.error == error("file does not exist 'missing.txt'")


def test_invoked_with_missing_file_absolute_path(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', dir('missing.txt')])
    # then
    assert output.error == error(f"file does not exist '{dir('missing.txt')}'")


def test_invoked_with_missing_file_relative_path(application: Application):
    # given
    with directory('directory') as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', '../not-this/../missing.txt'])
    # then
    assert output.error == error("file does not exist '../missing.txt'")


def test_invoked_with_missing_file_current_relative_path(application: Application):
    # given
    with directory('directory') as dir:
        # when
        output = application.run(dir(), ['--to', 'lf', '../child/./missing.txt'])
    # then
    assert output.error == error("file does not exist '../child/missing.txt'")
