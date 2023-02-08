from test.fixture.application import Application


def test_invoked_with_missing_file(application: Application):
    # when
    output = application.run(['missing.txt'])
    # then
    assert output.error == """usage: crlf [-h] filename
crlf: error: file does not exist 'missing.txt'
"""
