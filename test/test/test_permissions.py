from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import restricted


def test_failed_restricted_file(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', 'line\n')
        with dir.permissions(['file.txt'], 0):
            # when
            output = application.run(dir(), ['--to', 'lf', 'file.txt'])
        # then
        assert output.text == restricted(['file.txt'])


def test_failed_restricted_files(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/one.txt', 'line\n')
        dir.store('directory/two.txt', 'line\n')
        with dir.permissions(['directory/one.txt', 'directory/two.txt'], 0):
            # when
            output = application.run(dir(), ['--to', 'lf', 'directory'])
        # then
        assert output.text == restricted([
            'directory/one.txt',
            'directory/two.txt'
        ])
