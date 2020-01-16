import logging
import os
import re
import time
from pathlib import Path
from typing import Dict

SECONDS_PER_DAY = 24 * 60 * 60


def delete(path: Path, shred: bool) -> None:
    """Delete the file at the given path.

    If ``shred`` is True, first write over the file with random data before deleting.
    """
    if shred:
        with open(path, "ba+") as fil:
            length = fil.tell()
            fil.seek(0)
            fil.write(os.urandom(length))

    Path(path).unlink()


def sweep(name: str, path: Path, opts: Dict, dry_run: bool) -> None:
    # pylint: disable = too-many-arguments
    """Remove old files from a directory

    :name:    Name of the section being cleaned
    :path:    Path to remove files from
    :opts:    Dict of options containing the following:

                num_days     - Remove files older than this many days
                ignore       - Regular expression pattern of paths to ignore
                match        - Regular expression pattern of paths to remove
                trash        - If set, move files to this directory instead of deleting
                               them
                shred        - Securely delete file data before removing
                remove_empty - Remove empty subdirectories

    :dry_run: Only show what would happen without actually doing anything

    """
    logging.info("Sweeping %s", name)
    num_seconds = opts["num_days"] * SECONDS_PER_DAY
    thresh = time.time() - num_seconds
    match, ignore = opts["match"], opts["ignore"]
    for root, dirs, files in os.walk(path):
        if opts["remove_empty"] and not dirs and not files:
            Path(root).rmdir()
            continue

        dirs[:] = [d for d in dirs if re.match(match, d) and not re.match(ignore, d)]
        files = [f for f in files if re.match(match, f) and not re.match(ignore, f)]
        for fil in files:
            fpath = Path(root).joinpath(fil)
            if not fpath.exists():
                continue

            if fpath.stat().st_mtime >= thresh:
                continue

            if opts["trash"]:
                logging.info("Moving %s to %s", fpath, opts["trash"])
                if not dry_run:
                    fpath.rename(Path(opts["trash"]).joinpath(fpath.name))
            else:
                if opts["shred"]:
                    logging.info("Securely deleting %s", fpath)
                else:
                    logging.info("Deleting %s", fpath)

                if not dry_run:
                    delete(fpath, opts["shred"])
