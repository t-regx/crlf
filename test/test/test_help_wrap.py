from test.fixture.application import Application
from test.fixture.directory import directory


def test_help_wide(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--help'], width=120)
    # then
    assert output.text == """usage: crlf [-h] [-V] [-q | -s] [-d] [-R] --to {crlf,lf} filename

Tool to change line endings of text files

positional arguments:
  filename        path to a file or directory

options:
  -h, --help      show this help message
  -V, --version   show version
  -q, --quiet     change line endings without batch output, only summary
  -s, --silent    change line endings without any output
  -d, --dry-run   do not actually modify files
  -R              recurse into nested directories
  --to {crlf,lf}  change line endings to CRLF or LF
"""


def test_help_narrow(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--help'], width=40)
    # then
    assert output.text == """usage: crlf [-h] [-V] [-q | -s] [-d]
            [-R] --to {crlf,lf}
            filename

Tool to change line endings of text
files

positional arguments:
  filename        path to a file or
                  directory

options:
  -h, --help      show this help
                  message
  -V, --version   show version
  -q, --quiet     change line endings
                  without batch
                  output, only summary
  -s, --silent    change line endings
                  without any output
  -d, --dry-run   do not actually
                  modify files
  -R              recurse into nested
                  directories
  --to {crlf,lf}  change line endings
                  to CRLF or LF
"""


def test_help_extra_narrow(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--help'], width=20)
    # then
    assert output.text == """usage: crlf [-h]
            [-V]
            [-q | -s]
            [-d]
            [-R]
            --to
            {crlf,lf}
            filename

Tool to change
line endings of
text files

positional arguments:
  filename
    path to a file
    or directory

options:
  -h, --help
    show this help
    message
  -V, --version
    show version
  -q, --quiet
    change line
    endings
    without batch
    output, only
    summary
  -s, --silent
    change line
    endings
    without any
    output
  -d, --dry-run
    do not
    actually
    modify files
  -R
    recurse into
    nested
    directories
  --to {crlf,lf}
    change line
    endings to
    CRLF or LF
"""
