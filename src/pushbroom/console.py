"""
Pushbroom entry point
"""
import argparse
import configparser
import fnmatch
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict

from pushbroom import __version__, sweep


def run() -> None:
    """Main entry point"""
    args = parse_args()
    setup_logging(args)
    config = read_config(args.config)
    pushbroom(config, args.dry_run)


def pushbroom(config: configparser.ConfigParser, dry_run: bool = False) -> None:
    """Run pushbroom"""
    logging.info("Starting pushbroom")
    for section in config.sections():
        path = config.get(section, "path")
        fullpath = Path(path).expanduser().absolute()
        if not fullpath.is_dir():
            logging.error("No such directory: %s", fullpath)
        else:
            opts = parse_opts(config, section)
            sweep(section, fullpath, opts, dry_run)


def parse_args() -> argparse.Namespace:
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


def setup_logging(args: argparse.Namespace) -> None:
    """Set up logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    stream_handler.setLevel(logging.ERROR)

    if not args.dry_run:
        # If not doing a dry run log, to a file
        log_file = (
            Path(os.environ.get("XDG_CACHE_HOME", Path("~/.cache").expanduser()))
            .joinpath("pushbroom")
            .joinpath("pushbroom.log")
        )
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(str(log_file))
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(fmt)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

    if args.verbose or args.dry_run:
        # If verbose or doing a dry run print info to console
        stream_handler.setLevel(logging.INFO)

    logger.addHandler(stream_handler)


def read_config(conf_file: Path = None) -> configparser.ConfigParser:
    """Find and read configuration file"""
    if not conf_file:
        # Look under XDG_CONFIG_HOME first, then for /etc/pushbroom/pushbroom.conf
        conf_file = (
            Path(os.environ.get("XDG_CONFIG_HOME", Path("~/.config").expanduser()))
            .joinpath("pushbroom")
            .joinpath("config")
        )
        if not conf_file.exists():
            conf_file = Path("/etc/pushbroom/pushbroom.conf")

    config = configparser.ConfigParser()
    try:
        with conf_file.open() as fil:
            config.read_file(fil)
    except FileNotFoundError:
        logging.error("Configuration file %s not found", conf_file)
        sys.exit(1)

    return config


def parse_opts(config: configparser.ConfigParser, section: str) -> Dict:
    num_days = config.getint(section, "numdays")
    trash_dir = config.get(section, "trash", fallback=None)
    ignore = config.get(section, "ignore", fallback="").split(",")
    ignore_re = re.compile("|".join([fnmatch.translate(x) for x in ignore]))
    match = config.get(section, "match", fallback="*").split(",")
    match_re = re.compile("|".join([fnmatch.translate(x) for x in match]))
    shred = config.getboolean(section, "shred", fallback=False)
    remove_empty = config.getboolean(section, "removeempty", fallback=True)

    trash = None
    if trash_dir:
        if shred:
            logging.warning("Ignoring 'Shred' option while 'Trash' is set")
            shred = False

        trash = Path(trash_dir).expanduser().absolute()
        if not trash.is_dir():
            logging.warning("Creating directory %s", trash)
            trash.mkdir(parents=True)

    return {
        "num_days": num_days,
        "ignore": ignore_re,
        "match": match_re,
        "trash": trash,
        "shred": shred,
        "remove_empty": remove_empty,
    }
