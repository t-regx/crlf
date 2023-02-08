from test.conftest import Application
from test.fixture.directory import directory


def test_convert_crlf_to_lf(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "line\r\n")
        # when
        application.run(dir(), ['file.txt'])
        # then
        assert dir.open('file.txt') == "line\n"


def test_convert_crlf_to_lf_multiline(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "one\r\ntwo\r\n")
        # when
        application.run(dir(), ['file.txt'])
        # then
        assert dir.open('file.txt') == "one\ntwo\n"


def test_convert_crlf_to_lf_log_output(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', 'line')
        # when
        output = application.run(dir(), ['file.txt'])
    # then
    assert output.text == "Corrected file file.txt\n"


def test_invoked_with_missing_file(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['missing.txt'])
    # then
    assert output.error == """usage: crlf [-h] filename
crlf: error: file does not exist 'missing.txt'
"""


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
    assert output.text == "Ignoring file improper.txt\n"
