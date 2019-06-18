import logging
import os
import re
import time

SECONDS_PER_DAY = 24 * 60 * 60


def sweep(path, num_days, ignored, trash=None, dry_run=False):
    """Remove old files from a directory

    :path: Path to remove files from
    :num_days: Remove files older than this many days
    :ignored: Regex pattern of paths to ignore
    :trash: If set, move files to this directory instead of deleting them

    """
    now = time.time()
    logging.info("Starting janitor")
    num_seconds = num_days * SECONDS_PER_DAY
    thresh = now - num_seconds
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not re.match(ignored, d)]

        files = [f for f in files if not re.match(ignored, f)]
        for file in files:
            fpath = os.path.join(root, file)
            if os.stat(fpath).st_mtime < thresh:
                if trash:
                    if dry_run:
                        print("Moving {} to {}".format(file, trash))
                    else:
                        logging.info("Moving %s to %s", file, trash)
                        os.rename(fpath, os.path.join(trash, file))
                else:
                    if dry_run:
                        print("Deleting {}".format(file))
                    else:
                        logging.info("Deleting %s", file)
                        os.remove(fpath)
