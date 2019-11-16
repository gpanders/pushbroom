import logging
import os
import re
import time

SECONDS_PER_DAY = 24 * 60 * 60


def delete(path, shred):
    if shred:
        with open(path, "ba+") as f:
            length = f.tell()
            f.seek(0)
            f.write(os.urandom(length))

    os.remove(path)


def sweep(name, path, num_days, ignore, match, trash, dry_run, shred):
    # pylint: disable = too-many-arguments
    """Remove old files from a directory

    :name:     Name of the section being cleaned
    :path:     Path to remove files from
    :num_days: Remove files older than this many days
    :ignore:   Regular expression pattern of paths to ignore
    :match:    Regular expression pattern of paths to remove
    :trash:    If set, move files to this directory instead of deleting them
    :dry_run:  Only show what would happen without actually doing anything
    :shred:    Securely delete file data before removing

    """
    logging.info("Sweeping %s", name)
    num_seconds = num_days * SECONDS_PER_DAY
    thresh = time.time() - num_seconds
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if re.match(match, d) and not re.match(ignore, d)]
        files = [f for f in files if re.match(match, f) and not re.match(ignore, f)]
        for file in files:
            fpath = os.path.join(root, file)
            if not os.path.exists(fpath):
                continue

            if os.stat(fpath).st_mtime >= thresh:
                continue

            if trash:
                logging.info("Moving %s to %s", fpath, trash)
                if not dry_run:
                    os.rename(fpath, os.path.join(trash, file))
            else:
                if shred:
                    logging.info("Securely deleting %s", fpath)
                else:
                    logging.info("Deleting %s", fpath)

                if not dry_run:
                    delete(fpath, shred)
