from .apply import Apply


def execute_from_command_line(command=None):
    """Run a Apply."""
    apply = Apply(command)
    apply.execute()
