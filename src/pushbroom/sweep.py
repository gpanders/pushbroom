import logging
import os
import re
import time

SECONDS_PER_DAY = 24 * 60 * 60


def sweep(path, num_days, ignored, trash=None, dry_run=False):
    """Remove old files from a directory

    :path: Path to remove files from
    :num_days: Remove files older than this many days
    :ignored: Glob pattern of paths to ignore
    :trash: If set, move files to this directory instead of deleting them
    :dry_run: Only show what would happen without actually doing anything

    """
    now = time.time()
    logging.info("Starting pushbroom")
    num_seconds = num_days * SECONDS_PER_DAY
    thresh = now - num_seconds
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not re.match(ignored, d)]

        files = [f for f in files if not re.match(ignored, f)]
        for file in files:
            fpath = os.path.join(root, file)
            try:
                if os.stat(fpath).st_mtime < thresh:
                    if trash:
                        logging.info("Moving %s to %s", fpath, trash)
                        if not dry_run:
                            os.rename(fpath, os.path.join(trash, file))
                    else:
                        logging.info("Deleting %s", fpath)
                        if not dry_run:
                            os.remove(fpath)
            except FileNotFoundError:
                pass
