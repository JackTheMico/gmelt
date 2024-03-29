from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Footer, Markdown, Header, Label, Input, Button

MDSTR = """\
# Welcome to Gmelt!
## Please follow the instructions below to configure Gmelt.
"""


class InitScreen(Screen):
    BINDINGS = [
        ("ctrl+b", "file_pick", "File Pick"),
        ("ctrl+h", "dir_pick", "Directory Pick"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(name="Gmelt", show_clock=True)
        yield Markdown(MDSTR)
        yield Label("Step 1: Select your Gmail credentials.json file.")
        with Horizontal():
            yield Input(
                placeholder="You can type the full path or use the right button to choose",
                id="credentials_input",
            )
            yield Button("File Pick", variant="success", id="credentials_browse")
        yield Button("Start Setup", variant="error", id="init")
        yield Footer()

    def action_file_pick(self) -> None:
        self.query_one("#credentials_browse").press()

    def action_dir_pick(self) -> None:
        self.query_one("#config_dir_browse").press()
