# Janitor
Bash script to automate deleting old files in a specified directory

# Installation
    git clone git@github.com:gpanders/Janitor.git
    cd Janitor
    ./install.sh

The install script creates a symlink in your home directory to `janitor.sh` and
appends an entry to the current user's `crontab` (use `crontab -l` to view your active cron jobs)
