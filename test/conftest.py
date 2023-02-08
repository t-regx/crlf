#
# This filename is special.
#
# We needed a place to store fixtures,
# to be able to reuse them between files, so that they're included
# no matter what test is currently being run.
# We could simply import them from a file, but "pytest" interface,
# is that of an implicit argument in the test file, making it detectable
# by any IDE as unused import (they're not being used, so IDE removes it).
# "pytest" should probably allow defining fixtures explicitly somehow.
#
# Anyway, the only way to initialize fixtures on run in "pytest" currently
# is to create "conftest.py", which is being (again, implicitly) used by
# pytest before each test.
#
# If there is a better way in "pytest" to reuse fixtures, this file should
# probably be deleted and fixtures moved to a proper place.
#
# Do not rename this file.
#
from _pytest.fixtures import SubRequest
from pytest import fixture, mark, param, Config, Item, Mark

from test.fixture.application import MemoryApplication, Application, ProcessApplication
from test.fixture.pytest.mark import memory, process, memoryonly


def pytest_configure(config: Config):
    config.addinivalue_line("markers", memory.name)


def pytest_collection_modifyitems(items: list[Item]):
    for item in list(items):
        if test_has_marker(item, memoryonly) and not test_has_marker(item, memory):
            items.remove(item)


def test_has_marker(item: Item, mark: Mark) -> bool:
    return item.get_closest_marker(mark.name) is not None


@fixture(params=[
    param(MemoryApplication, marks=memory),
    param(ProcessApplication, marks=[process, mark.slow])
])
def application(request: SubRequest) -> Application:
    return request.param()
