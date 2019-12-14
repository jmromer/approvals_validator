from contextlib import contextmanager
from exceptions import ProjectRootNotFoundError
from functools import lru_cache
from io import TextIOWrapper
from pathlib import Path
from typing import List, Set

OWNERS_FILE: str = "OWNERS"
DEPS_FILE: str = "DEPENDENCIES"
PROJECT_ROOT_FILES: List[str] = [
    ".git",
    "src/",
    "setup.py",
]


@contextmanager
def open_file(path: str):
    """Open and yield the file at the given `path`. Fail quietly."""
    try:
        with open(path, "r") as f:
            yield f
    except FileNotFoundError:
        yield ()


@lru_cache()
def owners_set(directory: Path) -> Set[str]:
    """
    Return the list of the owners for the given `directory`.
    """
    with open_file(f"{directory}/{OWNERS_FILE}") as f:
        lines = (line.rstrip() for line in f)
        return set(line for line in lines if line)


@lru_cache()
def approvers_set(directory: Path) -> Set[str]:
    """
    Return the potential approvers listing for the given `directory`.
    """
    curr_dir: Path = directory.absolute()
    proj_root: Path = project_root(directory)

    approvers = set()
    while True:
        approvers.update(owners_set(curr_dir))
        if curr_dir == proj_root:
            break
        curr_dir = curr_dir.parent
    return approvers


@lru_cache()
def dependencies_set(directory: Path) -> Set[str]:
    """Return the dependencies listing for the given `directory`."""
    with open_file(f"{directory}/{DEPS_FILE}") as f:
        lines = (line.rstrip() for line in f)
        return set(line for line in lines if line)


def containing_directory(file_object: TextIOWrapper) -> Path:
    """Return the directory containing the given file."""
    return Path(file_object.name).parent.absolute()


@lru_cache()
def is_project_root(directory: Path) -> bool:
    """Return True if the given `directory` is a project root."""
    for root_file in PROJECT_ROOT_FILES:
        if (directory.absolute() / root_file).exists():
            return True
    return False


@lru_cache()
def project_root(curr_dir: Path) -> Path:
    """
    Search up the file hiearchy from the current directory `curr_dir` for a
    project root, returning one if found.
    """
    target_dir = curr_dir
    curr_dir = curr_dir.expanduser().absolute()
    sys_root = Path("/")

    while not is_project_root(curr_dir) and curr_dir != sys_root:
        curr_dir = curr_dir.parent

    if curr_dir == sys_root:
        raise ProjectRootNotFoundError(target_dir)

    return curr_dir


@lru_cache()
def find_dependent_dirs(target_dir: Path) -> Set[Path]:
    """
    Find all project directories dependent on directory `target_dir`, including
    transitively dependent directories.

    Return a set of (absolute) Paths.
    """
    target_dir = target_dir.absolute()
    proj_root = project_root(target_dir)

    all_dep_dirs = set()
    curr_deps = set([target_dir.relative_to(proj_root)])

    while curr_deps:
        direct_deps = find_direct_dependent_dirs(
            from_root=proj_root,
            for_dir=curr_deps.pop(),
        )
        curr_deps.update(direct_deps)
        all_dep_dirs.update(curr_deps)

    return set([proj_root / d for d in all_dep_dirs])


@lru_cache()
def find_direct_dependent_dirs(for_dir: Path, from_root: Path) -> Set[Path]:
    """
    Collect all directories directly dependent on directory `for_dir`.
    Search from root directory `from_root`.

    Return a Set of Paths relative to the given project root.
    """
    target_dirname = str(for_dir)
    dependents = set()
    candidates = (df.parent for df in from_root.rglob(DEPS_FILE))

    for cand_dir in candidates:
        if target_dirname in dependencies_set(cand_dir):
            dependents.add(cand_dir.relative_to(from_root))
    return dependents
