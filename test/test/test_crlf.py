from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.pytest.mark import memoryonly
from test.fixture.usage import error


def test_reline_crlf_to_lf(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        application.run(dir(), ['file.txt'])
        # then
        assert dir.open('file.txt') == "line\n"


def test_reline_crlf_to_lf_multiline(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "one\r\ntwo\r\n")
        # when
        application.run(dir(), ['file.txt'])
        # then
        assert dir.open('file.txt') == "one\ntwo\n"


def test_reline_crlf_to_lf_log_output(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', 'line')
        # when
        output = application.run(dir(), ['file.txt'])
    # then
    assert output.text == "Updated: file.txt\n"


@memoryonly
def test_invoked_with_empty_filename(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), [''])
    # then
    assert output.error == error("file does not exist ''")


def test_invoked_with_missing_file(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['missing.txt'])
    # then
    assert output.error == error("file does not exist 'missing.txt'")


def test_ignore_file_with_improper_encoding(application: Application):
    # given
    with directory() as dir:
        dir.store('improper.txt', b'\x1f\x7f\xee \x0d\x0a')
        # when
        application.run(dir(), ['improper.txt'])
        # then
        assert dir.open_bytes('improper.txt') == b'\x1f\x7f\xee \x0d\x0a'


def test_ignore_file_with_improper_encoding_log_output(application: Application):
    # given
    with directory() as dir:
        dir.store('improper.txt', b'\x1f\x7f\xee')
        # when
        output = application.run(dir(), ['improper.txt'])
    # then
    assert output.text == """Failed:  improper.txt
         ^ ! expected unicode encoding, malformed encoding found
"""


def test_reline_crlf_to_lf_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', "line\r\nline")
        # when
        application.run(dir(), ['directory'])
        # then
        assert dir.open('directory/file1.txt') == "line\nline"


def test_reline_crlf_to_lf_directory_log_output(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', 'line')
        # when
        output = application.run(dir(), ['directory'])
    # then
    assert output.text == "Updated: directory/file1.txt\n"


def test_reline_crlf_to_lf_directory_many(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', "line\r\nline")
        dir.store('directory/file2.txt', "line\r\nline")
        # when
        application.run(dir(), ['directory'])
        # then
        assert dir.open('directory/file1.txt') == "line\nline"
        assert dir.open('directory/file2.txt') == "line\nline"


def test_reline_crlf_to_lf_directory_many_log_output(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', "line\r\nline")
        dir.store('directory/file2.txt', "line\r\nline")
        # when
        output = application.run(dir(), ['directory'])
    # then
    assert output.text == "Updated: directory/file1.txt\nUpdated: directory/file2.txt\n"


def test_reline_crlf_to_lf_subdirectory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file1.txt', "line\r\nline")
        dir.store('one/two/file2.txt', "line\r\nline")
        # when
        application.run(dir(), ['one/two'])
        # then
        assert dir.open('one/two/file1.txt') == "line\nline"
        assert dir.open('one/two/file2.txt') == "line\nline"


def test_reline_crlf_to_lf_subdirectory_log_output(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file1.txt', "line\r\nline")
        dir.store('one/two/file2.txt', "line\r\nline")
        # when
        output = application.run(dir(), ['one/two'])
    # then
    assert output.text == "Updated: one/two/file1.txt\nUpdated: one/two/file2.txt\n"


def test_ignore_directory_with_improper_encoding(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/improper.txt', b'\x1f\x7f\xee \x0d\x0a')
        # when
        application.run(dir(), ['directory'])
        # then
        assert dir.open_bytes('directory/improper.txt') == b'\x1f\x7f\xee \x0d\x0a'


def test_ignore_directory_with_improper_encoding_log_output(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/improper.txt', b'\x1f\x7f\xee')
        # when
        output = application.run(dir(), ['directory'])
    # then
    assert output.text == """Failed:  directory/improper.txt
         ^ ! expected unicode encoding, malformed encoding found
"""


def test_not_reline_nested_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file.txt', "line\r\n")
        # when
        application.run(dir(), ['one'])
        # then
        assert dir.open('one/two/file.txt') == "line\r\n"


def test_not_reline_crlf_directory_log_output(application: Application):
    # given
    with directory() as dir:
        dir.store('one/two/file.txt', "line\r\n")
        # when
        output = application.run(dir(), ['one'])
    # then
    assert output.text == ""


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
