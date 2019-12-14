from exceptions import ProjectRootNotFoundError
from pathlib import Path

import pytest

import file_utils as utils


def test_project_root(data_dir):
    curr_file = (data_dir / "minimal" / "y" / "file")
    root = utils.project_root(curr_file)
    assert root == (data_dir / "minimal").absolute()


def test_project_root_search_fails():
    curr_dir = Path("~").expanduser().absolute()
    with pytest.raises(ProjectRootNotFoundError) as excinfo:
        utils.project_root(curr_dir)
        assert excinfo.match("Project root search failed")
        assert excinfo.match(curr_dir)


def test_is_project_root(data_dir):
    assert not utils.is_project_root(data_dir)
    assert utils.is_project_root(data_dir / "..")
    assert utils.is_project_root(data_dir / "minimal")
    assert not utils.is_project_root(data_dir / "minimal" / "y")


def test_containing_directory(changed_file_y, project_root):
    cwd = utils.containing_directory(changed_file_y)
    proj_root = project_root.absolute()
    assert cwd.relative_to(proj_root) == Path("data/minimal/y")


def test_find_dependent_dirs_search_failure():
    curr_dir = Path("~").expanduser().absolute()
    with pytest.raises(ProjectRootNotFoundError) as excinfo:
        utils.find_dependent_dirs(curr_dir)
        assert excinfo.match("Project root search failed")
        assert excinfo.match(curr_dir)


def test_find_dependent_dirs(changed_file_y, data_dir):
    curr_dir = Path(changed_file_y.name).parent

    dependents = utils.find_dependent_dirs(curr_dir)
    assert len(dependents) == 2

    dep_dir = data_dir / "minimal" / "x"
    assert dep_dir in dependents

    trans_dep = data_dir / "minimal" / "z"
    assert trans_dep in dependents


def test_find_direct_dependent_dirs(data_dir):
    proj_root = data_dir / "minimal"
    curr_dir = Path("y")
    dependents = utils.find_direct_dependent_dirs(curr_dir, proj_root)
    assert dependents == {Path("x")}


def test_owners_set(changed_file_message):
    """
    Return a set containing owners defined in the same directory.
    """
    curr_dir = Path(changed_file_message.name).parent
    approvers = utils.owners_set(curr_dir)
    assert approvers == {"eclarke", "kantonelli"}


def test_approvers_set(changed_file_message):
    """
    Return a set containing owners defined in the same directory or any parent
    directory as the target file.
    """
    curr_dir = Path(changed_file_message.name).parent
    approvers = utils.approvers_set(curr_dir)
    assert approvers == {"eclarke", "ghopper", "kantonelli"}


def test_open_found_file():
    path = Path("data/minimal/y/OWNERS")
    with utils.open_file(path) as f:
        lines = [l.rstrip() for l in f.read().rstrip().split("\n")]
        assert lines == ["B", "C"]


def test_open_not_found_file_fails_gracefully():
    path = Path("data/minimal/y/MORE_OWNERS")
    with utils.open_file(path) as f:
        assert not f
