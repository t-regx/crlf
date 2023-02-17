from test.conftest import Application
from test.fixture.directory import directory


def test_ignore_crlf_file(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "file\n")
        # when
        output = application.run(dir(), ['file.txt'])
    # then
    assert output.text == """Ignored: file.txt
         ^ file already has LF line endings
"""


def test_ignore_crlf_file_absolute_path(application: Application):
    # given
    with directory() as dir:
        dir.store('file.txt', "file\n")
        # when
        output = application.run(dir(), [dir('file.txt')])
    # then
    assert output.text == f"""Ignored: {dir('file.txt')}
         ^ file already has LF line endings
"""


def test_ignore_crlf_file_parent_path(application: Application):
    # given
    with directory() as dir:
        dir.create('root')
        dir.store('file.txt', "file\n")
        # when
        output = application.run(dir('root'), ['../file.txt'])
    # then
    assert output.text == """Ignored: ../file.txt
         ^ file already has LF line endings
"""


def test_ignore_crlf_file_relative_path(application: Application):
    # given
    with directory('directory') as dir:
        dir.create('root')
        dir.store('folder/file.txt', "file\n")
        # when
        output = application.run(dir('root'), ['../not-this/../folder/file.txt'])
    # then
    assert output.text == """Ignored: ../folder/file.txt
         ^ file already has LF line endings
"""


def test_ignore_crlf_file_relative_path_file_current(application: Application):
    # given
    with directory('directory') as dir:
        dir.create('root')
        dir.store('folder/file.txt', "file\n")
        # when
        output = application.run(dir('root'), ['../folder/./file.txt'])
    # then
    assert output.text == """Ignored: ../folder/file.txt
         ^ file already has LF line endings
"""


def test_ignore_crlf_directory(application: Application):
    # given
    with directory() as dir:
        dir.store('directory/file1.txt', "file\n")
        dir.store('directory/file2.txt', "file\n")
        # when
        output = application.run(dir(), ['directory'])
    # then
    assert output.text == """Ignored: directory/file1.txt
         ^ file already has LF line endings
Ignored: directory/file2.txt
         ^ file already has LF line endings
"""
