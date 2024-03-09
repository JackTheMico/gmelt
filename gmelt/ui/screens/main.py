from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import ListView, ListItem, Label, Footer, Placeholder


class MainScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def gmailapi(self):
        return self.app.gmailapi

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ListView(
                *[ListItem(Label(label["name"])) for label in self.gmailapi.labels]
            )
            with VerticalScroll():
                yield Placeholder("Email titles")
        yield Footer()
