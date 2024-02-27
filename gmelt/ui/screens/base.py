from textual.app import ComposeResult
from textual.containers import Grid
from textual.events import Key as KeyEvent
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Footer


class ConfirmScreen(ModalScreen[bool]):
    """Screen with a dialog to quit."""

    def __init__(
        self,
        question: str = "Are you sure about this?",
        confirm: str = "[Y]es",
        cancel: str = "[N]o",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.question = question
        self.confirm = confirm
        self.cancel = cancel

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.question),
            Button(self.confirm, variant="error", id="confirm"),
            Button(self.cancel, variant="primary", id="cancel"),
            id="dialog",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.dismiss(True)
        elif event.button.id == "cancel":
            self.dismiss(False)

    def on_key(self, event: KeyEvent) -> None:
        if event.key == self.confirm[1].lower():
            self.dismiss(True)
        elif event.key == self.cancel[1].lower():
            self.dismiss(False)
