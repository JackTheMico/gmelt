from textual.app import App
from textual.css.query import NoMatches
from gmelt.ui.screens import (
    InitScreen,
    MainScreen,
    QuitScreen,
    SelectScreen,
    ConfirmScreen,
)
from textual.widgets import Button, DirectoryTree
from confz.exceptions import FileException
from gmelt.config.config import (
    GmeltConfig,
    DEFAULT_CONFIG_TOML,
    GMELT_CONFIG_HOME,
)
from gmelt.utils.config import create_config
from gmelt.api.gmail import GmailApi


class Gmelt(App):
    CSS_PATH = "tui.tcss"
    BINDINGS = [
        ("ctrl+q", "request_quit", "Quit"),
    ]

    SCREENS = {
        "init": InitScreen(name="init"),
        "quit": QuitScreen(name="quit"),
        "main": MainScreen(name="main"),
        "confirm": ConfirmScreen(name="confirm"),
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.init = False
        try:
            self.config = GmeltConfig()
        except FileException:
            self.init = True
            self.conf = create_config(GMELT_CONFIG_HOME, DEFAULT_CONFIG_TOML)
        else:
            self.gmailapi = GmailApi(GMELT_CONFIG_HOME, self.config.credentials_path)
            self.gmailapi.authenticate()

    async def on_mount(self) -> None:
        if self.init:
            self.push_screen("init")
        elif self.gmailapi.status:
            self.push_screen("main")

    def action_request_quit(self) -> None:
        def check_quit(quit: bool) -> None:
            if quit:
                self.exit()

        self.push_screen("quit", check_quit)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()

        if event.button.id == "credentials_browse":
            self.push_screen(
                SelectScreen("Select your credentials.json file", id="credentials")
            )
        elif event.button.id == "config_dir_browse":
            self.push_screen(
                SelectScreen("Select configuration directory", id="directory")
            )
        elif event.button.id == "init":
            self.gmailapi = GmailApi(GMELT_CONFIG_HOME, self.config.credentials_path)
            self.push_screen("main")

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        event.stop()

        def check_confirm(confirm: bool) -> None:
            try:
                screen = self.query_one("#credentials")
            except NoMatches:
                self.notify("Please only select the directory ❗❗❗")
                return
            if confirm and screen:
                self.conf.write(f'credentials_path="{str(event.path)}"')
                self.conf.close()
                self.config = GmeltConfig()
                self.gmailapi = GmailApi(
                    GMELT_CONFIG_HOME, self.config.credentials_path
                )
                self.creds = self.gmailapi.authenticate()
                # NOTE: must pop screen first, then query the element.
                self.pop_screen()
                self.query_one("#credentials_input").value = str(event.path)

        self.push_screen("confirm", check_confirm)

    # def on_directory_tree_directory_selected(
    #     self, event: DirectoryTree.DirectorySelected
    # ) -> None:
    #     event.stop()

    #     def check_confirm(confirm: bool) -> None:
    #         try:
    #             screen = self.query_one("#directory")
    #         except NoMatches:
    #             self.notify("Please only select the credentials.json file ❗❗❗")
    #             return
    #         if confirm and screen:
    #             self.config_dir = str(event.path)
    #             # NOTE: must pop screen first, then query the element.
    #             self.pop_screen()
    #             self.query_one("#config_dir_input").value = str(event.path)

    #     self.push_screen("confirm", check_confirm)


if __name__ == "__main__":
    app = Gmelt(init=True)
    app.run()
