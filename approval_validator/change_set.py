from functools import cached_property
from io import TextIOWrapper
from typing import Iterator, Tuple

from changed_directory import ChangedDirectory


class ChangeSet:
    def __init__(self, approvers: Tuple[str],
                 changed_files: Tuple[TextIOWrapper]):
        self.approvals_received = approvers
        self.changed_files = changed_files

    @property
    def affected_directories(self) -> Iterator[ChangedDirectory]:
        """
        Iterator for the directories affected by the change set.
        Includes transitively affected directories.
        """
        return (ChangedDirectory(cf, approvals=self.approvals_received)
                for cf in self.changed_files)

    @cached_property
    def approved(self) -> bool:
        """
        Return True if all affected directories have received sufficient
        approvals.
        """
        return all(d.approved for d in self.affected_directories)
