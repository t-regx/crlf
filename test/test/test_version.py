from test.conftest import Application
from test.fixture.directory import directory


def test_version(application: Application):
    # given
    with directory() as dir:
        # when
        output = application.run(dir(), ['--version'])
    # then
    assert output.text == "1.0.0\n"
