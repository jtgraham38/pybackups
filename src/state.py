"""
Manages the state.json file that controls the service.
"""

from pathlib import Path
import json
import os

STATE_DIR = Path(os.environ.get("STATE_DIRECTORY", Path("/var/lib/pybackups")))


class InitStateException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GetStateException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ValidateStateException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def init_state(state_path=f"{STATE_DIR}/state.json"):
    # create a path from the passed in path
    state_path = Path(state_path)

    # ensure the path ends in .json
    if not state_path.suffix == ".json":
        raise InitStateException("The state file path must end in .json!")

    # if the file already exists, return early
    if state_path.exists() and state_path.is_file():
        print("State already exists!")
        return

    # if the config path's parent directory does not exist, or is not a directory, return early
    config_destination_path = Path(__file__).resolve().parents[1]
    if (not config_destination_path.exists()) or (not config_destination_path.is_dir()):
        return

    # pull the default content from service/default_config.json
    default_path = (
        Path(__file__).resolve().parents[1] / "service" / "default_state.json"
    )
    default_content = ""
    with default_path.open("r") as f:
        default_content = json.load(f)

    # if default content was found, continue
    if not default_content:
        raise InitStateException("No default config found!")

    # write the default content to the state path
    with state_path.open("w", encoding="utf-8") as f:
        json.dump(default_content, f, indent=4, ensure_ascii=False)

    print("State initialized successfully!")


def get_state(state_path=f"{STATE_DIR}/state.json"):
    # load the passed in file, and return its json content
    # create a path from the passed in path
    state_path = Path(state_path)

    # ensure the path ends in .json
    if not state_path.suffix == ".json":
        raise GetStateException("The state file path must end in .json!")

    # if the file already exists, return early
    if (not state_path.exists()) or (not state_path.is_file()):
        return

    # open the file, and read and return its contents
    default_content = ""
    with state_path.open("r") as f:
        default_content = json.load(f)

    print("State gotten successfully!")
    return default_content


def save_state(state, state_path=f"{STATE_DIR}/state.json"):
    # create a path from the passed in path
    state_path = Path(state_path)

    # ensure the path ends in .json
    if not state_path.suffix == ".json":
        raise InitStateException("The state file path must end in .json!")

    # write the default content to the state path
    with state_path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

    print("State saved successfully!")


def validate_state(state):
    try:
        json.dumps(state)
    except (TypeError, OverflowError):
        raise ValidateStateException("State must be json-encodable!")

    if "jobs" not in state:
        raise ValidateStateException("There is no state section for copy jobs!")

    # validate each copy job in the state
    for _id, job in state["jobs"].items():
        if "backups" not in job:
            raise ValidateStateException(f"Job {_id} is missing a 'count' value!")

        # validate each backup in the backups state
        for i, backup in enumerate(job["backups"]):
            if "archive_file" not in backup:
                raise ValidateStateException(
                    f"Job {_id}, archive {i} is missing an 'archive_file' value!"
                )
            if "created_at" not in backup:
                raise ValidateStateException(
                    f"Job {_id}, archive {i} is missing a 'created_at' value!"
                )

    print("State is valid!")
