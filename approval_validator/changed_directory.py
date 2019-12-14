from functools import cached_property
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, Tuple

import file_utils as util


class ChangedDirectory:
    def __init__(self,
                 changed_file: TextIOWrapper,
                 approvals: Optional[Tuple[str, ...]] = None):
        self._changed_file = changed_file
        self._approvals_received: Tuple[str, ...] = approvals or tuple()

    @property
    def impacted_directories(self) -> Tuple[Path, ...]:
        return (self.directory, *self.affected_directories)

    @cached_property
    def directory(self) -> Path:
        return util.containing_directory(self._changed_file)

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

    def __change_approved(self, directory: Path) -> bool:
        """
        Return True if directory has no owners or if an approval has been
        received from any owner.
        """
        owners = util.approvers_set(directory)
        if not owners:
            return True
        approvals = owners.intersection(self._approvals_received)
        return len(approvals) > 0
