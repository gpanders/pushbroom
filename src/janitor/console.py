import argparse
import configparser
import fnmatch
import logging
import os
import sys

import janitor

LOG_FILE = os.path.expanduser("~/.cache/janitor/janitor.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename=LOG_FILE,
)


def run():
    """Run janitor"""
    parser = argparse.ArgumentParser(description="Clean up your filesystem.")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="path to config file",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="show what would be done without actually doing anything",
    )

    args = parser.parse_args()

    if not args.config:
        # Look under XDG_CONFIG_HOME first, then look for ~/.janitorrc
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        args.config = os.path.join(xdg_config_home, "janitor", "config")
        if not os.path.exists(args.config):
            args.config = os.path.expanduser("~/.janitorrc")

    config = configparser.ConfigParser()
    try:
        with open(args.config, "r") as f:
            config.read_file(f)
    except FileNotFoundError:
        print("Configuration file {} not found".format(args.config))
        sys.exit(1)

    for path in config.sections():
        fullpath = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(fullpath):
            logging.error("No such directory: %s", fullpath)
        else:
            num_days = config.getint(path, "numdays")
            trash = config.get(path, "trash", fallback=None)
            ignore = config.get(path, "ignore", fallback="").split(",")
            ignored = r"|".join([fnmatch.translate(x) for x in ignore])

            if trash:
                trash = os.path.abspath(os.path.expanduser(trash))
                if not os.path.isdir(trash):
                    logging.error("No such directory %s", trash)

            janitor.sweep(fullpath, num_days, ignored, trash, args.dry_run)
