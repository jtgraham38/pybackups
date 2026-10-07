"""
Manages the config.json file that controls the service.
"""

from pathlib import Path
import json
import os

CONFIG_DIR = Path(os.environ.get("CONFIGURATION_DIRECTORY", Path("/etc/pybackups")))


class InitConfigException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GetConfigException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ValidateConfigException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def init_config(config_path=f"{CONFIG_DIR}/config.json"):
    # create a path from the passed in path
    config_path = Path(config_path)

    # ensure the path ends in .json
    if not config_path.suffix == ".json":
        raise InitConfigException("The config file path must end in .json!")

    # if the file already exists, return early
    if config_path.exists() and config_path.is_file():
        print("Config already exists!")
        return

    # if the config path's parent directory does not exist, or is not a directory, return early
    config_destination_path = Path(__file__).resolve().parents[1]
    if (not config_destination_path.exists()) or (not config_destination_path.is_dir()):
        return

    # pull the default content from service/default_config.json
    default_path = (
        Path(__file__).resolve().parents[1] / "service" / "default_config.json"
    )
    default_content = ""
    with default_path.open("r") as f:
        default_content = json.load(f)

    # if default content was found, continue
    if not default_content:
        raise InitConfigException("No default config found!")

    # write the default content to the config path
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(default_content, f, indent=4, ensure_ascii=False)

    print("Config initialized successfully!")


def get_config(config_path=f"{CONFIG_DIR}/config.json"):
    # load the passed in file, and return its json content
    # create a path from the passed in path
    config_path = Path(config_path)

    # ensure the path ends in .json
    if not config_path.suffix == ".json":
        raise GetConfigException("The config file path must end in .json!")

    # if the file already exists, return early
    if (not config_path.exists()) or (not config_path.is_file()):
        return

    # open the file, and read and return its contents
    default_content = ""
    with config_path.open("r") as f:
        default_content = json.load(f)

    print("Config gotten successfully!")
    return default_content


def validate_config(config):

    try:
        json.dumps(config)
    except (TypeError, OverflowError):
        raise ValidateConfigException("Config must be json-encodable!")

    if not config["jobs"]:
        raise ValidateConfigException("You have not configured any copy jobs!")

    # validate each copy job in the config
    for i, job in enumerate(config["jobs"]):
        if "id" not in job:
            raise ValidateConfigException(f"Job {i} config is missing an 'id' setting!")
        if "interval" not in job:
            raise ValidateConfigException(
                f"Job {i} config is missing an 'interval' setting!"
            )
        if "target" not in job:
            raise ValidateConfigException(
                f"Job {i} config is missing a 'target' setting!"
            )
        if "max" not in job:
            raise ValidateConfigException(f"Job {i} config is missing a 'max' setting!")
        if "destination" not in job:
            raise ValidateConfigException(
                f"Job {i} config is missing an 'destination' setting!"
            )
        if "options" not in job:
            raise ValidateConfigException(
                f"Job {i} config is mising an 'options' setting!"
            )

    print("Config is valid!")
