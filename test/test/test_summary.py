from test.conftest import Application
from test.fixture.directory import directory
from test.fixture.usage import malformed


def test_summary(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/malformed.txt', b'\x1f\x7f\xee \x0d\x0a')
        dir.store('directory/ignored.txt', "line\n")
        dir.store('directory/regular.txt', "line\r\n")
        # when
        output = application.run(dir(), ['directory'])
        # then
        assert output.text == """Ignored: directory/ignored.txt
         ^ file already has LF line endings
Failed:  directory/malformed.txt
         ^ ! expected unicode encoding, malformed encoding found
Updated: directory/regular.txt
Done. Updated: 1 files, ignored: 1 files, and encountered malformed: 1 files.
"""


def test_summary_many(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/first/malformed.txt', b'\x1f\x7f\xee \x0d\x0a')
        dir.store('directory/first/ignored.txt', "line\n")
        dir.store('directory/first/regular.txt', "line\r\n")
        dir.store('directory/second/ignored.txt', "line\n")
        dir.store('directory/regular.txt', "line\r\n")
        # when
        output = application.run(dir(), ['-R', 'directory'])
        # then
        assert output.text.endswith("Done. Updated: 2 files, ignored: 2 files, and encountered malformed: 1 files.\n")


def test_stat_improper_encoding(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/first.txt', b'\x1f\x7f\xee \x0d\x0a')
        dir.store('directory/second.txt', b'\x1f\x7f\xee \x0d\x0a')
        # when
        output = application.run(dir(), ['directory'])
        # then
        assert output.text == malformed([
            'directory/first.txt',
            'directory/second.txt',
        ])
