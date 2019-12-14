from inspect import cleandoc


class ApprovalValidatorError(Exception):
    pass


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
