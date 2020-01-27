# pylint: disable = redefined-outer-name
"""
Pushbroom unit tests
"""
import configparser
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from pushbroom import console

TRASH_DIR = Path("~/.cache/pushbroom/trash").expanduser()


def get_config(name: str):
    """
    Read the given configuration file and return the configuration object
    """
    conf_file = Path(__file__).parent.joinpath("configs").joinpath(name)
    return console.read_config(conf_file)


def get_config_path(config):
    """
    Retrieve the absolute, expanded path from the given configuration object
    """
    section = config.sections()[0]
    return Path(config.get(section, "path")).expanduser().absolute()


def make_test_file(path: Path, name: str = None):
    """
    Create a file with the given ``name`` under the given ``path``. Set the file's
    mtime to two days ago.
    """
    if not name:
        name = "test.txt"

    path.mkdir(parents=True, exist_ok=True)
    test_file = path.joinpath(name)
    test_file.touch()
    mtime = (datetime.today() - timedelta(2)).timestamp()
    os.utime(str(test_file), (mtime, mtime))
    return test_file


@pytest.fixture
def trash_dir():
    """
    Create and provide the path to the trash directory.
    Delete the directory and all of its contents after use.
    """
    TRASH_DIR.mkdir(parents=True, exist_ok=True)
    yield TRASH_DIR
    shutil.rmtree(str(TRASH_DIR))


def test_tilde_home(monkeypatch):
    """
    Paths with a tilde should expand to the user's home directory
    """
    config = get_config("home.conf")

    def mock_sweep(name, path, *args, **kwargs):
        # pylint: disable = unused-argument
        assert Path(path) == Path.home()

    monkeypatch.setattr(console, "sweep", mock_sweep)
    console.pushbroom(config, dry_run=True)


def test_required_options():
    """
    If any required options are missing, an exception should be raised
    """
    config = get_config("missing_path.conf")
    with pytest.raises(configparser.NoOptionError):
        console.pushbroom(config)

    config = get_config("missing_numdays.conf")
    path = get_config_path(config)
    path.mkdir(parents=True, exist_ok=True)
    with pytest.raises(configparser.NoOptionError):
        console.pushbroom(config)
    path.rmdir()


def test_dry_run():
    """
    Running with dry_run=True should not delete anything.
    Running without dry_run=True should delete the file.
    """
    config = get_config("delete.conf")
    path = get_config_path(config)
    test_file = make_test_file(path)

    console.pushbroom(config, dry_run=True)
    assert test_file.exists()

    console.pushbroom(config)
    assert not test_file.exists()

    path.rmdir()


def test_ignore():
    """
    Files matching the Ignore pattern should not be deleted
    """
    config = get_config("ignore.conf")
    path = get_config_path(config)
    ignored_file = make_test_file(path, "ignored.txt")
    not_ignored_file = make_test_file(path, "not_ignored.txt")

    console.pushbroom(config)
    assert ignored_file.exists()
    assert not not_ignored_file.exists()

    ignored_file.unlink()
    path.rmdir()


def test_match():
    """
    Only files matching the Match pattern should be deleted
    """
    config = get_config("match.conf")
    path = get_config_path(config)
    matched_file = make_test_file(path, "matched.txt")
    not_matched_file = make_test_file(path, "not_matched.txt")

    console.pushbroom(config)
    assert not matched_file.exists()
    assert not_matched_file.exists()

    not_matched_file.unlink()
    path.rmdir()


def test_match_with_ignore():
    """
    When both Match and Ignore are specified, only files that match the Match pattern
    but not the Ignore pattern should be deleted
    """
    config = get_config("match_and_ignore.conf")
    path = get_config_path(config)
    ignored_file = make_test_file(path, "ignored.txt")
    matched_file = make_test_file(path, "matched.txt")

    console.pushbroom(config)
    assert ignored_file.exists()
    assert not matched_file.exists()

    ignored_file.unlink()
    path.rmdir()


def test_trash(trash_dir: Path):
    """
    File should be moved to the Trash dir and not deleted
    """
    config = get_config("trash.conf")
    path = get_config_path(config)
    test_file = make_test_file(path, "file_to_go_in_trash.txt")

    console.pushbroom(config)
    assert not test_file.exists()
    assert trash_dir.joinpath(test_file.name).exists()

    path.rmdir()


def test_shred_with_trash(trash_dir: Path):
    """
    When both Shred and Trash are specified, Shred should be ignored
    """
    config = get_config("shred_and_trash.conf")
    path = get_config_path(config)
    test_file = make_test_file(path, "shred_and_trash.txt")

    mtime = test_file.stat().st_mtime
    with test_file.open("w", encoding="utf8") as fil:
        fil.write("Hello, world!")

    # Force mtime back to what it was
    os.utime(str(test_file), (mtime, mtime))

    console.pushbroom(config)
    assert not test_file.exists()
    assert trash_dir.joinpath(test_file.name).exists()

    with trash_dir.joinpath(test_file.name).open(encoding="utf8") as fil:
        assert "Hello, world!" in fil.readlines()

    path.rmdir()


def test_remove_empty_dirs():
    """
    Empty directories should be removed
    """
    config = get_config("delete.conf")
    path = get_config_path(config)

    empty = path.joinpath("empty")
    empty.mkdir(parents=True)

    assert empty.exists()
    console.pushbroom(config)
    assert not empty.exists()

    path.rmdir()


def test_no_remove_empty_dirs():
    """
    Empty directories should not be removed when RemoveEmpty is false
    """
    config = get_config("no_remove_empty.conf")
    path = get_config_path(config)

    empty = path.joinpath("empty")
    empty.mkdir(parents=True)

    console.pushbroom(config)
    assert empty.exists()

    empty.rmdir()
    path.rmdir()
