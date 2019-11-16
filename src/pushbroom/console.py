import argparse
import configparser
import fnmatch
import logging
import os
import re
import sys

from pushbroom import sweep, __version__

def run():
    args = parse_args()
    setup_logging(args)
    config = read_config(args.config)
    pushbroom(config, args.dry_run)


def pushbroom(config, dry_run=False):
    """Run pushbroom"""
    logging.info("Starting pushbroom")
    for section in config.sections():
        path = config.get(section, "path")
        fullpath = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(fullpath):
            logging.error("No such directory: %s", fullpath)
        else:
            num_days = config.getint(section, "numdays")
            trash = config.get(section, "trash", fallback=None)
            ignore = config.get(section, "ignore", fallback="").split(",")
            ignore_re = re.compile("|".join([fnmatch.translate(x) for x in ignore]))
            match = config.get(section, "match", fallback="*").split(",")
            match_re = re.compile("|".join([fnmatch.translate(x) for x in match]))
            shred = config.get(section, "shred", fallback=False)

            if trash:
                if shred:
                    logging.warning("Ignoring 'Shred' option while 'Trash' is set")
                    shred = False

                trash = os.path.abspath(os.path.expanduser(trash))
                if not os.path.isdir(trash):
                    logging.error("No such directory %s", trash)

            sweep(
                section, fullpath, num_days, ignore_re, match_re, trash, dry_run, shred
            )


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Clean up your filesystem.")
    parser.add_argument("-c", "--config", type=str, help="path to config file")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="show what would be done without actually doing anything",
    )

    return parser.parse_args()


def setup_logging(args):
    """Set up logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(message)s"))
    ch.setLevel(logging.ERROR)

    if not args.dry_run:
        # If not doing a dry run log, to a file
        log_file = os.path.join(
            os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")),
            "pushbroom",
            "pushbroom.log",
        )
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

    if args.verbose or args.dry_run:
        # If verbose or doing a dry run print info to console
        ch.setLevel(logging.INFO)

    logger.addHandler(ch)


def read_config(conf_file=None):
    """Find and read configuration file"""
    if not conf_file:
        # Look under XDG_CONFIG_HOME first, then look for ~/.pushbroomrc
        conf_file = os.path.join(
            os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
            "pushbroom",
            "config",
        )
        if not os.path.exists(conf_file):
            conf_file = os.path.expanduser("~/.pushbroomrc")

    config = configparser.ConfigParser()
    try:
        with open(conf_file, "r") as f:
            config.read_file(f)
    except FileNotFoundError:
        logging.error("Configuration file %s not found", conf_file)
        sys.exit(1)

    return config
