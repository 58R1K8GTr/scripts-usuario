"""Abstract methods."""


from abc import ABC, abstractmethod
from unittest.mock import Mock

from i3ipc import Con
from i3ipc.model import Rect
from rich import print as rich_print


class Window(ABC):
    """Represents a window."""
    @abstractmethod
    def __init__(self, con: Con) -> None:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Get window name."""

    @abstractmethod
    def set_focus(self) -> 'Window':
        """Focus this window."""

    @abstractmethod
    def set_mark(self, mark_name: str) -> 'Window':
        """Mark this window."""

    @abstractmethod
    def set_unmark(self, mark_name: str) -> 'Window':
        """Unmark this window."""

    @abstractmethod
    def invert_status_float(self) -> 'Window':
        """Invert status of floating mode."""

    @abstractmethod
    def enable_float(self) -> 'Window':
        """Enable floating mode."""

    @abstractmethod
    def resize(self, size: str) -> 'Window':
        """Resize this window with a determined size."""

    @abstractmethod
    def move(self, location: str) -> 'Window':
        """Move a window to a determinated place."""

    @abstractmethod
    def marks(self) -> list[str]:
        """Returns the marks of this window."""

    @property
    @abstractmethod
    def mark(self) -> str:
        """Returns the mark of this window."""

    @abstractmethod
    def focused(self) -> bool:
        """Returns if it is focused."""

    @property
    @abstractmethod
    def rect(self) -> Rect:
        """Returns rect window."""

    @property
    @abstractmethod
    def float_type(self) -> str:
        """Returns float type."""

    @abstractmethod
    def enable_sticky(self) -> 'Window':
        """Enable sticky mode."""

    @abstractmethod
    def disable_sticky(self) -> 'Window':
        """Disable sticky mode."""

    @abstractmethod
    def execute(self) -> None:
        """Execute all commands."""


class NoWindowCon(Window):
    """This is not a window."""

    def __init__(self, *_) -> None:
        self.__default_message = 'log {}: [red]No window selected.[/]'

    def __default_execution(self, method_name: str = '') -> None:
        rich_print(self.__default_message.format(method_name))

    @property
    def name(self) -> str:
        self.__default_execution('name')
        return ''

    def set_focus(self) -> 'Window':
        self.__default_execution('set_focus')
        return self

    def set_mark(self, mark_name: str) -> 'Window':
        self.__default_execution('set_mark')
        return self

    def set_unmark(self, mark_name: str) -> 'Window':
        self.__default_execution('set_unmark')
        return self

    def invert_status_float(self) -> 'Window':
        self.__default_execution('invert_status_float')
        return self

    def enable_float(self) -> 'Window':
        self.__default_execution('enable_float')
        return self

    def move(self, location: str) -> 'Window':
        self.__default_execution('move')
        return self

    def resize(self, size: str) -> 'Window':
        self.__default_execution('resize')
        return self

    def marks(self) -> list[str]:
        self.__default_execution('marks')
        return []

    @property
    def mark(self) -> str:
        self.__default_execution('mark')
        return ''

    def focused(self) -> bool:
        self.__default_execution('focused')
        return False

    @property
    def rect(self) -> Mock:
        self.__default_execution('rect')
        return Mock(spec=Rect)

    @property
    def float_type(self) -> str:
        self.__default_execution('float_type')
        return ''

    def enable_sticky(self) -> 'Window':
        self.__default_execution('enable_sticky')
        return self

    def disable_sticky(self) -> 'Window':
        self.__default_execution('disable_sticky')
        return self

    def execute(self) -> None:
        self.__default_execution('execute')


class WindowCon(Window):
    """Manager a window."""

    def __init__(self, con: Con):
        self.__con = con
        self.__commands = []

    @property
    def name(self) -> str:
        return self.__con.name  # type: ignore

    def set_focus(self) -> 'Window':
        self.__commands.append('focus')
        return self

    def set_mark(self, mark_name: str) -> 'Window':
        self.__commands.append(f'mark {mark_name}')
        return self

    def set_unmark(self, mark_name: str) -> 'Window':
        self.__commands.append(f'unmark {mark_name}')
        return self

    def invert_status_float(self) -> 'Window':
        self.__commands.append("floating toggle")
        return self

    def enable_float(self) -> 'Window':
        self.__commands.append("floating enable")
        return self

    def move(self, location: str) -> 'Window':
        rect = self.__con.rect
        base = f"{rect.x} {rect.y}"
        if location.endswith(base):
            return self
        self.__commands.append(f"move {location}")
        return self

    def resize(self, size: str) -> 'Window':
        self.__commands.append(f"resize set {size}")
        return self

    def marks(self) -> list[str]:
        return self.__con.marks

    @property
    def mark(self) -> str:
        marks = self.__con.marks
        if len(marks) == 0:
            return ''
        return marks[0]

    def focused(self) -> bool:
        return self.__con.focused  # type: ignore

    @property
    def rect(self) -> Rect:
        return self.__con.rect

    @property
    def float_type(self) -> str:
        return self.mark.split('_')[0]

    def enable_sticky(self) -> 'Window':
        self.__commands.append('sticky enable')
        return self

    def disable_sticky(self) -> 'Window':
        self.__commands.append('sticky disable')
        return self

    def execute(self) -> None:
        self.__con.command(', '.join(self.__commands))
        self.__commands = []
