"""
Copies a directory, and all its subfolders, to a given destination.
"""

import zipfile
from datetime import datetime as dt
from pathlib import Path


class ZipJobException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DelJobException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# make a zip archive of the target in the destination
def zip_job(target, destination, options={}):
    # make path objects from the strings
    target_path = Path(target)
    destination_path = Path(destination)

    # generate a backup filename
    backup_name = Path(
        f"{dt.now().strftime('%Y-%m-%d-%H-%M-%S-%f')}_{target_path.name}.zip"
    )
    destination_file_path = destination_path / backup_name

    # ensure target exists
    if not (target_path.exists()):
        raise ZipJobException(f"Target path for job does not exist: {target_path}")

    # ensure destination does not exist, but its parent does
    if not destination_path.exists():
        raise ZipJobException(f"Destination path does not exist: {destination_path}")

    if destination_file_path.exists():
        raise ZipJobException(
            f"Destination file path already exists: {destination_file_path}"
        )

    # prep cpignore key
    cpignore = [Path(ignore_path) for ignore_path in options.get("cpignore")]

    # zip the target into the destination
    with zipfile.ZipFile(destination_file_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for target_entry_path in sorted(target_path.rglob("*")):
            # skip excluded files and folders
            target_entry_path = Path(target_entry_path)
            relative_entry_path = target_entry_path.relative_to(target_path)

            # skip files and folders in the cpignore
            should_continue = False
            for ignore_path in cpignore:
                if relative_entry_path.is_relative_to(ignore_path):
                    should_continue = True
                    break
            if should_continue:
                print(f"Ignoring folder/directory: {relative_entry_path}")
                continue

            # write an target_entry_path to the zip archive
            print(f"Adding file: {target_entry_path}")
            zf.write(
                target_entry_path, target_entry_path.relative_to(target_path.parent)
            )

        print(f"Finished writing archive {destination_file_path}")
        return destination_file_path


# remove the target archive
def del_job(target):
    target_path = Path(target)

    # ensure target exists and is a file
    if not (target_path.is_file()):
        raise DelJobException(f"Target path for job does not exist: {target_path}")

    # delete the target file
    target_path.unlink()
    print(f"Deleted {target} successfully!")
