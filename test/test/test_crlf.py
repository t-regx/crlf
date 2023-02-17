from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import error, updated, malformed, summary


def test_reline_crlf_to_lf(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['file.txt'])
        # then
        assert dir.open('file.txt') == "line\n"
        assert output.text == updated(['file.txt'])


def test_reline_crlf_to_lf_multiline(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "first\r\nsecond\r\n")
        # when
        application.run(dir(), ['file.txt'])
        # then
        assert dir.open('file.txt') == "first\nsecond\n"


def test_ignore_file_with_improper_encoding(application: Application):
    # given
    with directory() as dir:
        dir.store('improper.txt', b'\x1f\x7f\xee \x0d\x0a')
        # when
        output = application.run(dir(), ['improper.txt'])
        # then
        assert dir.open_bytes('improper.txt') == b'\x1f\x7f\xee \x0d\x0a'
        assert output.text == malformed(['improper.txt'])


def test_reline_crlf_to_lf_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', "line\r\nline")
        # when
        output = application.run(dir(), ['directory'])
        # then
        assert dir.open('directory/file1.txt') == "line\nline"
        assert output.text == updated(['directory/file1.txt'])


def test_reline_crlf_to_lf_directory_many(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', "line\r\nline")
        dir.store('directory/file2.txt', "line\r\nline")
        # when
        output = application.run(dir(), ['directory'])
        # then
        assert dir.open('directory/file1.txt') == "line\nline"
        assert dir.open('directory/file2.txt') == "line\nline"
        assert output.text == updated(["directory/file1.txt", "directory/file2.txt"])


def test_reline_crlf_to_lf_subdirectory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file1.txt', "line\r\nline")
        dir.store('one/two/file2.txt', "line\r\nline")
        # when
        output = application.run(dir(), ['one/two'])
        # then
        assert dir.open('one/two/file1.txt') == "line\nline"
        assert dir.open('one/two/file2.txt') == "line\nline"
        assert output.text == updated(['one/two/file1.txt', 'one/two/file2.txt'])


def test_ignore_directory_with_improper_encoding(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/improper.txt', b'\x1f\x7f\xee \x0d\x0a')
        # when
        output = application.run(dir(), ['directory'])
        # then
        assert dir.open_bytes('directory/improper.txt') == b'\x1f\x7f\xee \x0d\x0a'
        assert output.text == malformed(['directory/improper.txt'])


def test_not_reline_nested_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['one'])
        # then
        assert dir.open('one/two/file.txt') == "line\r\n"
        assert output.text == summary()


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
