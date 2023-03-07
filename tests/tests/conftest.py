from pytest import fixture
from tests.infra.api import API


@fixture(scope='session')
def api():
    return API()
