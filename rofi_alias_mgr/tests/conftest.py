from pytest import fixture
from pathlib import Path


@fixture
def mock_path():
    return Path("/mock/path")
