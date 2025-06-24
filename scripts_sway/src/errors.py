"""Handling errors."""


from contextlib import contextmanager

from rich import print as rich_print


@contextmanager
def catch_value_error():
    """Catch value error."""
    try:
        yield
    except ValueError as e:
        rich_print(f'[red]Error: {e}[/]')
