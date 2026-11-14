from copy import deepcopy
import pytest
from soloos.onboarding import demo


@pytest.fixture
def business():
    return deepcopy(demo())
