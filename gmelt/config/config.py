import os
from confz import BaseConfig, FileSource

HOME = os.getenv("HOME", "")
XDG_CONFIG_HOME = os.getenv("XDG_CONFIG_HOME", os.path.join(HOME, ".config"))
GMELT_CONFIG_HOME = os.path.join(XDG_CONFIG_HOME, "gmelt")
DEFAULT_CONFIG_TOML = os.path.join(GMELT_CONFIG_HOME, "gmelt.toml")
DEFAULT_CREDENTIALS_JSON = os.path.join(GMELT_CONFIG_HOME, "credentials.json")


class GmeltConfig(BaseConfig):
    credentials_json_path: str

    CONFIG_SOURCES = [
        FileSource(file=DEFAULT_CONFIG_TOML),
    ]
