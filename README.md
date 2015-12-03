# Janitor
Bash script to automate deleting old files in a specified directory

## Installation
    git clone git@github.com:gpanders/Janitor.git
    cd Janitor
    ./install.sh

The install script creates a symlink in your home directory to `janitor.sh` and
appends an entry to the current user's `crontab` (use `crontab -l` to view your active cron jobs)

## Options

Open the `janitor.sh` file to change options

| Option           | Description                                                                                                      |
|:----------------:| ---------------------------------------------------------------------------------------------------------------- |
| **TARGET_DIR**   | Define which folder to clean out                                                                                 |
| **DAYS_TO_KEEP** | How long should a file be able to live in the folder?                                                            |
| **TRASH_DIR**    | Where to move deleted files. Delete this if you want to permanently delete files instead of moving them to Trash |
| **LOG_DIR**      | Location to store log files, relative to the Janitor directory                                                   |
