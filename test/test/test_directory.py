from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import updated


def test_crlf_nested_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/a/b/file.txt', "line\r\n")
        dir.store('one/two/c/d/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '-R', 'one/two'])
        # then
        assert dir.open('one/two/a/b/file.txt') == "line\n"
        assert output.text == updated([
            "one/two/a/b/file.txt",
            "one/two/c/d/file.txt"
        ])


def test_crlf_nested_directory_trailing_separator(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/three/four/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '-R', 'one/two/'])
        # then
        assert dir.open('one/two/three/four/file.txt') == "line\n"
        assert output.text == updated(['one/two/three/four/file.txt'])


def test_crlf_nested_directory_trailing_separators(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/three/four/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '-R', 'one///'])
        # then
        assert dir.open('one/two/three/four/file.txt') == "line\n"
        assert output.text == updated(['one/two/three/four/file.txt'])


def test_crlf_parent(application: Application):
    # given
    with directory('directory') as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '../directory/file.txt'])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == updated(['../directory/file.txt'])


def test_crlf_parent_directory(application: Application):
    # given
    with directory('directory') as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '../directory/'])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == updated(['../directory/file.txt'])


def test_crlf_parent_directory_recurse(application: Application):
    # given
    with directory('directory') as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '-R', '../directory/'])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == updated(['../directory/file.txt'])


def test_crlf_parent_and_relative(application: Application):
    # given
    with directory('directory') as dir:
        dir.store('child/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['--to', 'lf', '../directory/child/../child/file.txt'])
        # then
        assert dir.open('child/file.txt') == "line\n"
        assert output.text == updated(['../directory/child/file.txt'])
