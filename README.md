# Pushbroom

Pushbroom is a tool designed to help keep your filesystem clear of clutter.
Certain directories, such as your downloads directory, tend to accumulate a
large amount of old files that take up space. Over time, this clutter can
accumulate to a significant amount of storage space. Pushbroom gives you an easy
way to remove these old files.

Pushbroom is written in Python and should therefore work on any platform that
can run Python. For now, it is only officially supported for macOS and Linux.

## Installation

### Homebrew (macOS only)

Install via Homebrew:

    brew install gpanders/tap/pushbroom

Copy and modify the included `pushbroom.conf` file to
`~/.config/pushbroom/config` and use `brew services start
gpanders/tap/pushbroom` to start the automatic launchd daemon:

    cp -n /usr/local/etc/pushbroom.conf ~/.config/pushbroom/config
    brew services start gpanders/tap/pushbroom

Pushbroom will run once every hour.

### PyPI

Install using pip:

    pip install --user pushbroom

### From source

Check the [releases](https://github.com/gpanders/pushbroom/releases) page for
the latest release. Extract the archive and copy the files to their correct
locations:

    tar xzf pushbroom-vX.Y.Z.tar.gz
    cd pushbroom-vX.Y.Z
    cp -r bin /usr/local/
    cp -n pushbroom.conf ~/.config/pushbroom/config

## Usage

Pushbroom can be run from the command line using:

    pushbroom

Use `pushbroom --help` to see a list of command line options.

## Configuration

The Pushbroom configuration file is organized into sections where each section
represents a directory path to monitor. The default configuration file looks
like this:

    [Downloads]
    Path = ~/Downloads
    Trash = ~/.Trash
    NumDays = 30

This means that, by default, Pushbroom will monitor your ~/Downloads folder and
move any file or folder older than 30 days into your ~/.Trash directory.

If you don't want to move files into ~/.Trash but instead want to just delete
them, simply remove the `Trash` option:

    [Downloads]
    Path = ~/Downloads
    NumDays = 30

The name of the section (`Downloads` in this example) is not important and can
be anything you want:

    [Home Directory]
    Path = ~
    NumDays = 90

You can also specify an `Ignore` parameter to instruct Pushbroom to ignore any
files or directories that match the given glob:

    [Downloads]
    Path = ~/Downloads
    NumDays = 30
    Ignore = folder_to_keep/**/*

The following configuration items are recognized in `pushbroom.conf`:

**Path**

Specify which directory to monitor

**Trash**

Specify where to move files after deletion. If this option is not provided,
files will simply be deleted.

**NumDays**

Number of days to keep files in `Path` before they are removed.

**Ignore**

Glob expression pattern of files or directories to ignore.

## Automating

If installed via Homebrew then Pushbroom can be set to run once every hour using

    brew services start gpanders/tap/pushbroom

Another option is to install a crontab entry

    0 */1 * * * /usr/local/bin/pushbroom

If you are using a Linux distribution that uses systemd, you can copy the
[systemd service
file](https://github.com/gpanders/pushbroom/blob/master/contrib/systemd/pushbroom.service)
to `~/.local/share/systemd/` and enable the service with

    systemctl --user enable --now pushbroom

Note that you may need to change the path to the `pushbroom` script in the
service file depending on your method of installation.

## Similar Work

- [Belvedere](https://github.com/mshorts/belvedere): An automated file manager
  for Windows
- [Hazel](https://www.noodlesoft.com/): Automated Organization for your Mac
