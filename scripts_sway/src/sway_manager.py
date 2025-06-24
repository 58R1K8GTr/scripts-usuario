"""Sway windows management."""

from i3ipc import Connection

from src.windows import Window, WindowCon, NoWindowCon
from src.types_project import MarkType
from src.group_format_window import HorizontalLineState
from src.types_project import MarkSizeType, NumberPosition


class SwayManager:
    """Manager sway float windows."""

    # __init__ is now private and only assigns pre-computed values.
    def __init__(
        self, con: Connection, rect: tuple[int, int], mark_sizes: MarkSizeType
    ):
        self.__con = con
        self.__rect = rect
        self.__mark_sizes = mark_sizes
        self.__state = HorizontalLineState(
            self.__rect, self.__mark_sizes, NumberPosition(1, 1)
        )

    @classmethod
    def create(cls, con: Connection) -> "SwayManager":
        """Asynchronously create and initialize a SwayManager instance."""
        outputs = con.get_outputs()
        output = next(filter(lambda x: x.active, outputs))
        rect = (output.rect.width, output.rect.height)
        mark_sizes: MarkSizeType = {
            'popup': list(map(lambda x: x // 100 * 20, rect)),
            'medium': list(map(lambda x: x // 100 * 40, rect)),
            'large': list(map(lambda x: x // 100 * 60, rect))
        }
        return cls(con, rect, mark_sizes)

    def get_windows_by_mark(self, mark_name: MarkType) -> list[WindowCon]:
        """Returns popup windows."""
        pattern = f"{mark_name}_.*"
        tree_root = self.__con.get_tree()
        marked_containers = tree_root.find_marked(pattern)
        marked_containers = list(map(
            WindowCon, filter(lambda x: x.pid is not None, marked_containers)
        ))
        marked_containers.sort(key=lambda x: int(x.mark.split('_')[-1]))
        return marked_containers

    @property
    def mark_names(self) -> list[MarkType]:
        """Return names of marks."""
        return list(self.__mark_sizes.keys())

    def _get_focused_window(self) -> Window:
        """Return a focused window."""
        focused = (self.__con.get_tree()).find_focused()
        if focused and focused.pid is not None:
            return WindowCon(focused)
        return NoWindowCon()

    def __generate_new_mark_name(self, name: MarkType) -> str:
        """Generate a new mark name."""
        marked_names = list(filter(
            lambda x: x.startswith(f"{name}_"),
            sorted(self.__con.get_marks())
        ))
        if len(marked_names) == 0:
            return f"{name}_1"
        last_number = int(marked_names[-1].split('_')[-1])
        new_number = last_number + 1
        return f"{name}_{new_number}"

    def transform_focused_as(self,  mark_name: MarkType) -> Window:
        """Transform the currently focused window as some window form."""
        window = self._get_focused_window()
        if bool(window.mark):
            return NoWindowCon()
        mark_sizes = self.__mark_sizes[mark_name]
        size = f"width {mark_sizes[0]} height {mark_sizes[1]}"
        window.set_mark(
            self.__generate_new_mark_name(mark_name)
        ).enable_float().resize(size).execute()
        return window

    def transform_as_popup(self) -> None:
        """Transform the currently focused window as popup."""
        window = self.transform_focused_as('popup')
        window.enable_sticky().execute()

    def transform_as_medium(self) -> None:
        """Transform the currently focused window as medium."""
        self.transform_focused_as('medium')

    def transform_as_large(self) -> None:
        """Transform the currently focused window as large."""
        self.transform_focused_as('large')

    def move_left(self, mark_name: MarkType) -> None:
        """Move items to left."""
        self.__state.move_left()
        self.__state.organize(
            self.get_windows_by_mark(mark_name), mark_name
        )

    def move_right(self, mark_name: MarkType) -> None:
        """Move items to right."""
        self.__state.move_right()
        self.__state.organize(self.get_windows_by_mark(mark_name), mark_name)

    def move_up(self, mark_name: MarkType) -> None:
        """Move items to up."""
        self.__state.move_up()
        self.__state.organize(self.get_windows_by_mark(mark_name), mark_name)

    def move_down(self, mark_name: MarkType) -> None:
        """Move items to down."""
        self.__state.move_down()
        self.__state.organize(self.get_windows_by_mark(mark_name), mark_name)

    def organize_popup(self) -> None:
        """Organize popup windows."""
        self.__state.organize(self.get_windows_by_mark('popup'), 'popup')

        # Uso:
        # manager = SwayManager()
        # for win in manager.list_windows():
        #     print(win.name)
        # manager.focus_window_by_name("Terminal")

        # botar um bindsym para quando fechar a janela, ele verificar se ela
        # foi marcada e remover ela das marcas automaticamente.
        # para fazer isso, devo implementar o dunder contains na window?

        # agora a janela começa no x=1, y=1 (canto inferior direito)
        # pois faz mais sentido matemático.

        # o que dá para marcar:
        # Janelas (windows)
        # Workspaces
        # Containers (splits horizontais/verticais, grupos de janelas)
        # Floating windows

        # manter janelas visíveis em todos os workspaces: sticky enable
        # como pegar a janela focada via coneção?
        # trocar a organização individual por multipla com o self.organize?

        # assincronismo não é necessário.
