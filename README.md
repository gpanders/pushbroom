# Pushbroom
Keep select filesystem paths free of clutter

## Installation

Directly from source:

    git clone https://github.com/gpanders/pushbroom
    pip install ./pushbroom

Or from PyPI:

    pip install pushbroom

Pushbroom comes with an example configuration file `pushbroom.conf`. You can
copy this to either `$XDG_CONFIG_HOME/pushbroom/config` or `$HOME/.pushbroomrc` and
modify it to your needs.

## Configuration

The following configuration items are recognized in `pushbroom.conf`:

**Path**

Specify which directory to monitor

**Trash**

Specify where to move files after deletion. If this option is not provided,
files will simply be deleted.

**NumDays**

Number of days to keep files in `Path` before they are removed.

**Ignore**

Regular expression pattern of files or directories to ignore.
