from contextlib import contextmanager
from pathlib import Path

import pytest


@contextmanager
def fixture_file(path_rel_to_data_dir):
    fixture_path = Path(".") / "data" / path_rel_to_data_dir
    with open(fixture_path) as f:
        yield f


@pytest.fixture
def changed_file_y():
    with fixture_file("minimal/y/file") as cf:
        yield cf


@pytest.fixture
def changed_file_tweet():
    with fixture_file("repo/src/com/twitter/tweet/Tweet.java") as cf:
        yield cf


@pytest.fixture
def changed_file_user():
    with fixture_file("repo/src/com/twitter/user/User.java") as cf:
        yield cf


@pytest.fixture
def changed_file_follow():
    with fixture_file("repo/src/com/twitter/follow/Follow.java") as cf:
        yield cf


@pytest.fixture
def changed_file_message():
    with fixture_file("repo/src/com/twitter/message/Message.java") as cf:
        yield cf


@pytest.fixture
def project_root():
    return Path(".").absolute()


@pytest.fixture
def data_dir(project_root):
    return (project_root / "data")
