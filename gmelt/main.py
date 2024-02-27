import os
import sys
import typer
from confz.exceptions import FileException
from confz import FileSource
from gmelt.config.config import (
    GmeltConfig,
    DEFAULT_CONFIG_TOML,
    GMELT_CONFIG_HOME,
)
from gmelt.utils.asynctyper import AsyncTyper
from typing_extensions import Annotated
from loguru import logger
from gmelt.ui.tui import Gmelt


app = AsyncTyper()
state = {"verbose": False}


def setup_configuration(config_file="") -> GmeltConfig:
    CONFIG_SOURCES = []
    try:
        if not config_file:
            config = GmeltConfig()
        else:
            CONFIG_SOURCES.append(FileSource(file=config_file))
            config = GmeltConfig(CONFIG_SOURCES)
    except FileException:
        logger.error("🙏Please run init command first❗❗❗")
        sys.exit(1)
    else:
        return config


@app.command()
def start(
    config_file: Annotated[
        str, typer.Option(help="Gmelt configuration file path")
    ] = DEFAULT_CONFIG_TOML,
):
    if state["verbose"]:
        logger.debug(f"Config file: {config_file}")
    if not os.path.isdir(GMELT_CONFIG_HOME):
        os.mkdir(GMELT_CONFIG_HOME)
    if not os.path.exists(DEFAULT_CONFIG_TOML):
        tapp = Gmelt(init=True)
        tapp.run()
