# Janitor
Bash script to automate deleting old files in a specified directory

## Installation
    git clone git@github.com:gpanders/Janitor.git
    cd Janitor
    ./install.sh

By default, Janitor will monitor `$HOME/Downloads` and move any file older than
30 days to your Trash folder (`$HOME/.Trash`). These settings can be changed using
the installation script (see below).

## Options

**Target directory**

  Specify which directory to monitor

    -d <directory>

**Trash directory**

  Specify where to move files after deletion (if `-x` option is not set)

    -t <directory>

**Number of days to keep files**

    -n <integer>

**Hard delete files**

  Flag indicating to not move files to another directory, but rather permanently delete them

    -x
