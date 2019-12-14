from typing import Optional, Tuple

import click


def split_list(csv_string: Optional[str] = None) -> Tuple[str, ...]:
    """Split the given `csv_string`, returning a list of its entries."""
    entries = (csv_string or "").split(",")
    return tuple(entry for entry in entries if entry.strip())


class FileList(click.ParamType):
    name = "file_paths"
    file_arg = click.File()

    def convert(self, csv_string, param, ctx):
        return [
            self.file_arg.convert(filepath, param, ctx)
            for filepath in split_list(csv_string)
        ]


class UsernameList(click.ParamType):
    name = "usernames"

    def convert(self, csv_string, param, ctx):
        return split_list(csv_string)
