from test.conftest import Application
from test.fixture.directory import directory


def test_crlf_nested_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/a/b/file.txt', "line\r\n")
        dir.store('one/two/c/d/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['-R', 'one/two'])
        # then
        assert dir.open('one/two/a/b/file.txt') == "line\n"
        assert output.text == "Updated: one/two/a/b/file.txt\n" \
                              "Updated: one/two/c/d/file.txt\n"


def test_crlf_nested_directory_trailing_separator(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/three/four/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['-R', 'one/two/'])
        # then
        assert dir.open('one/two/three/four/file.txt') == "line\n"
        assert output.text == "Updated: one/two/three/four/file.txt\n"


def test_crlf_nested_directory_trailing_separators(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/three/four/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['-R', 'one///'])
        # then
        assert dir.open('one/two/three/four/file.txt') == "line\n"
        assert output.text == "Updated: one/two/three/four/file.txt\n"


def test_crlf_parent(application: Application):
    # given
    with directory('directory') as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['../directory/file.txt'])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == "Updated: ../directory/file.txt\n"


def test_crlf_parent_directory(application: Application):
    # given
    with directory('directory') as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['../directory/'])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == "Updated: ../directory/file.txt\n"


def test_crlf_parent_directory_recurse(application: Application):
    # given
    with directory('directory') as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['-R', '../directory/'])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == "Updated: ../directory/file.txt\n"


def test_crlf_parent_and_relative(application: Application):
    # given
    with directory('directory') as dir:
        dir.store('one/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['../directory/one/../one/file.txt'])
        # then
        assert dir.open('one/file.txt') == "line\n"
        assert output.text == "Updated: ../directory/one/file.txt\n"
