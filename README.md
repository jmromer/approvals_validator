Approval Validator
==================

A CLI to validate that sufficient approvals have been received for a changeset
in the context of a project.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Approval Validator](#approval-validator)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Requirements](#requirements)
    - [Dependencies](#dependencies)
    - [Tests](#tests)
    - [Design Notes](#design-notes)
        - [`ChangeSet`, `ChangedDirectory`](#changeset-changeddirectory)
        - [`file_utils`](#fileutils)
        - [`exceptions`](#exceptions)
    - [Performance](#performance)

<!-- markdown-toc end -->

Installation
------------

The quickest way to use the tool in anger is to install it using `pip`:
`pip install approvals-validator`.

Alternatively, run the executable from the project root. Install dependencies
with `bin/setup`.

Usage
-----

```text
% validate_approvals --help

Usage: validate_approvals REQUIRED_FLAGS

  Validate that the correct approvals have been received to approve changes
  to the given files.

  Note: Multiple approvers and/or changed files can be passed as CSV strings.

  Example:

    validate_approvals --approvers alovelace,eclarke --changed-files src/com/twitter/follow/Follow.java

Options:
  -a, --approvers USERNAMES       Username(s) of approvals.  [required]
  -c, --changed-files FILE_PATHS  File paths. [required]
  -h, --help                      Show this message and exit.
```

Requirements
------------

- Python >= 3.8.0 (for `functools.cached_property`)

A `.tool-versions` file is included for [asdf][asdf] users.

[asdf]: https://github.com/asdf-vm/asdf

Dependencies
------------

- [click](https://github.com/pallets/click)
- [pytest](https://pytest.org/en/latest/)

The test-runner script (`./test`) will attempt to install dependencies in a
virtualenv at project root named `./env`.

For reference, `bin/setup` usage instructions:

```text
Usage:
  ./bin/setup [OPTIONS] ENV

Install dependencies for `validate_approvals` in a virtualenv at project root.

Available environments:

 dev     Install all dependencies
 prod    Install minimal dependencies for running `validate_approvals`
 test    Install minimal and test dependencies

Available options:

 --silent  Run without verbose output
```

Tests
-----

A test runner script is included to run the entire test suite and display code
coverage metrics. Pass the `--docker` flag to (re-)build a Docker image and
run tests with Docker.

Acceptances tests are written in Bash script, unit and integration tests in
Python with pytest.

```text
% ./test

Running acceptance tests...
./validate_approvals -c data/minimal/y/file -a B
./validate_approvals -c data/minimal/y/file -a A,C
./validate_approvals -c data/minimal/y/file -a D
./validate_approvals --approvers alovelace,ghopper --changed-files data/repo/src/com/twitter/follow/Follow.java,data/repo/src/com/twitter/user/User.java
./validate_approvals --approvers alovelace --changed-files data/repo/src/com/twitter/follow/Follow.java
./validate_approvals --approvers eclarke --changed-files data/repo/src/com/twitter/follow/Follow.java
./validate_approvals --approvers alovelace,eclarke --changed-files data/repo/src/com/twitter/follow/Follow.java
./validate_approvals --approvers mfox --changed-files data/repo/src/com/twitter/tweet/Tweet.java

Running pytest tests...

Running mypy on 11 files... done with status 0
Success: no issues found in 11 source files
...............................                                   [100%]

---------- coverage: platform darwin, python 3.8.0-final-0 -----------
Name                                                 Stmts   Miss  Cover
------------------------------------------------------------------------
approval_validator/__init__.py                           3      0   100%
approval_validator/change_set.py                        14     14     0%
approval_validator/changed_directory.py                 30      0   100%
approval_validator/cli_utils.py                         14     14     0%
approval_validator/exceptions.py                         9      2    78%
approval_validator/file_utils.py                        74      0   100%
approval_validator/tests/__init__.py                     0      0   100%
approval_validator/tests/changed_directory_test.py      37      0   100%
approval_validator/tests/file_utils_test.py             59      4    93%
------------------------------------------------------------------------
TOTAL                                                  240     34    86%
```

Design Notes
------------

The script entrypoint is the CLI function in the executable
`validate_approvals`.

The `approval_validator.cli_utils` module defines how arguments are parsed.

### `ChangeSet`, `ChangedDirectory`

The main classes are `ChangeSet` and `ChangedDirectory`.

The former models an entire changeset (i.e., all the files passed via the
`--changed-files` flag), the latter each individual entry in the list of files
passed to `--changed_files`.

```py
# approval_validator/changed_directory.py L24-37

@cached_property
def affected_directories(self) -> Tuple[Path, ...]:
    return util.find_dependent_dirs(self.directory)

@cached_property
def approved(self) -> bool:
    """
    Return true if sufficient approval has been received for this
    ChangedDirectory.
    """
    for impacted_dir in self.impacted_directories:
        if not self.__change_approved(impacted_dir):
            return False
    return True
```

### `file_utils`

File-parsing and directory-traversal logic is housed in the `file_utils` module.

### `exceptions`

Defines `ApprovalValidatorError`, the base class for library-specific
exceptions, and `ProjectRootNotFoundError`, which is raised when a project root
can't be found.

```py
# approval_validator/exceptions.py L8-20

class ProjectRootNotFoundError(ApprovalValidatorError):
    """Raised when a project root can't be found."""
    def __init__(self, start_dir):
        self.start_dir = start_dir

    def __str__(self):
        message = f"""
        Project root search failed. Started from: {self.start_dir}

        Note: We detect the presence of a project root using the entries of
        PROJECT_ROOT_FILES. (see: approval_validator/file_utils.py)
        """
        return f"\n\n{cleandoc(message)}"
```

Performance
-----------

Caching improved running time by ~20%. The following facilities are used:

- [`functools.cached_property`][cp]
- [`functools.lru_cache`][lru]

[cp]: https://docs.python.org/3/library/functools.html#functools.cached_property
[lru]: https://docs.python.org/3/library/functools.html#functools.lru_cache
