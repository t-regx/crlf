from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import malformed, summary


def test_not_reline_nested_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['one'])
        # then
        assert dir.open('one/two/file.txt') == "line\r\n"
        assert output.text == summary()


def test_ignore_file_with_improper_encoding(application: Application):
    # given
    with directory() as dir:
        dir.store('improper.txt', b'\x1f\x7f\xee \x0d\x0a')
        # when
        output = application.run(dir(), ['improper.txt'])
        # then
        assert dir.open_bytes('improper.txt') == b'\x1f\x7f\xee \x0d\x0a'
        assert output.text == malformed(['improper.txt'])


def test_ignore_directory_with_improper_encoding(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/improper.txt', b'\x1f\x7f\xee \x0d\x0a')
        # when
        output = application.run(dir(), ['directory'])
        # then
        assert dir.open_bytes('directory/improper.txt') == b'\x1f\x7f\xee \x0d\x0a'
        assert output.text == malformed(['directory/improper.txt'])
