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

    cp /usr/local/etc/pushbroom.conf ~/.config/pushbroom/config
    brew services start gpanders/tap/pushbroom

Pushbroom will run once every hour.

### pipx

Install using [pipx](https://pipxproject.github.io/pipx/):

    pipx install pushbroom

Copy the [example configuration
file](https://raw.githubusercontent.com/gpanders/pushbroom/master/pushbroom.conf)
to `~/.config/pushbroom/config` or create your own from scratch.

### From source

Check the [releases](https://github.com/gpanders/pushbroom/releases) page for
the latest release. Extract the archive and copy the files to their correct
locations:

    tar xzf pushbroom-vX.Y.Z.tar.gz
    cd pushbroom-vX.Y.Z
    cp bin/pushbroom /usr/local/bin/pushbroom
    cp pushbroom.conf ~/.config/pushbroom/config

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
    Ignore = folder_to_keep

Similarly, you can specify `Match` to have Pushbroom only remove files that
match one of the given patterns:

    [Vim Backup Directory]
    Path = ~/.cache/vim/backup
    NumDays = 90
    Match = *~

Both `Ignore` and `Match` can be a list of patterns separated by commas.

    [Home Directory]
    Path = ~
    NumDays = 365
    Match = .*
    Ignore = .local, .config, .cache, .vim

Note that `.*` **is not** a regular expression for "match everything", but
rather a _glob expression_ for "all files that start with a period".

The following configuration items are recognized in `pushbroom.conf`:

### Path
**Required**

Absolute path to a directory to monitor. Tildes (`~`) are expanded to the
user's home directory.

### Trash

Specify where to move files after deletion. If omitted, files will simply be
deleted.

### NumDays
**Required**

Number of days to keep files in `Path` before they are removed.

### Ignore
**Default**: None

List of glob expression patterns of files or directories to ignore.

### Match
**Default**: `*`

List of glob expression patterns of files or directories to remove. If omitted,
everything is removed.

### Shred
**Default**: False

Securely delete files before removing them. Note that this option is mutually
exclusive with the [`Trash`](#trash) option, with `Trash` taking precedence if
both options are used.

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
