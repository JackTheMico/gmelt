import os


def create_config(config_home, config_file):
    os.makedirs(config_home, exist_ok=True)
    conf = open(config_file, "w")
    return conf
