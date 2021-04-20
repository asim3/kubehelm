from .apply import Apply


def execute_from_command_line(argv=[]):
    """Run an Apply."""
    apply = Apply(argv)
    apply.execute()
