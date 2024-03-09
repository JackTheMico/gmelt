import typer
from gmelt.config.config import (
    DEFAULT_CONFIG_TOML,
)
from gmelt.utils.asynctyper import AsyncTyper
from typing_extensions import Annotated
from loguru import logger
from gmelt.ui.tui import Gmelt


app = AsyncTyper()
state = {"verbose": False}


@app.command()
def start(
    config_file: Annotated[
        str, typer.Option(help="Gmelt configuration file path")
    ] = DEFAULT_CONFIG_TOML,
):
    if state["verbose"]:
        logger.debug(f"Config file: {config_file}")
    tapp = Gmelt()
    tapp.run()
