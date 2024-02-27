from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import DirectoryTree, Footer, Header

from textual.binding import Binding
from gmelt.config.config import HOME


class VimDirectoryTree(DirectoryTree):
    BINDINGS = [
        Binding("space", "select_cursor", "Select", show=True),
        Binding("enter", "toggle_node", "Toggle", show=True),
        Binding("k", "cursor_up", "Cursor Up", show=True),
        Binding("j", "cursor_down", "Cursor Down", show=True),
    ]


class SelectScreen(ModalScreen[str]):
    def __init__(self, title: str, *args, **kwargs):
        super().__init__(title, *args, **kwargs)
        self.title = title

    def compose(self) -> ComposeResult:
        yield Header(self.title)
        yield VimDirectoryTree(HOME)
        yield Footer()
