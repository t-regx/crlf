from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import updated


def test_reline_to_lf(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\n")
        # when
        output = application.run(dir(), ['--to', 'crlf', 'file.txt'])
        # then
        assert dir.open('file.txt') == "line\r\n"
        assert output.text == updated(['file.txt'])


def test_reline_to_lf_multiline(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "first\nsecond\n")
        # when
        application.run(dir(), ['--to', 'crlf', 'file.txt'])
        # then
        assert dir.open('file.txt') == "first\r\nsecond\r\n"


def test_reline_to_lf_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', "line\nline")
        # when
        output = application.run(dir(), ['--to', 'crlf', 'directory'])
        # then
        assert dir.open('directory/file1.txt') == "line\r\nline"
        assert output.text == updated(['directory/file1.txt'])


def test_reline_to_lf_directory_many(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', "line\nline")
        dir.store('directory/file2.txt', "line\nline")
        # when
        output = application.run(dir(), ['--to', 'crlf', 'directory'])
        # then
        assert dir.open('directory/file1.txt') == "line\r\nline"
        assert dir.open('directory/file2.txt') == "line\r\nline"
        assert output.text == updated(["directory/file1.txt", "directory/file2.txt"])


def test_reline_to_lf_subdirectory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file1.txt', "line\nline")
        dir.store('one/two/file2.txt', "line\nline")
        # when
        output = application.run(dir(), ['--to', 'crlf', 'one/two'])
        # then
        assert dir.open('one/two/file1.txt') == "line\r\nline"
        assert dir.open('one/two/file2.txt') == "line\r\nline"
        assert output.text == updated(['one/two/file1.txt', 'one/two/file2.txt'])


def test_reline_mixed_endings(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "first\nsecond\r\nthird\r")
        # when
        output = application.run(dir(), ['--to', 'crlf', 'file.txt'])
        # then
        assert dir.open('file.txt') == "first\r\nsecond\r\nthird\r\n"
        assert output.text == updated(['file.txt'])
