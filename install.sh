#!/usr/bin/env bash

# Set defaults
TARGET_DIR=$HOME/Downloads
NUM_DAYS=30
TRASH_DIR=$HOME/.Trash

function print_usage() {
    echo "Usage: ./install.sh [-x] [-d <target directory>] [-t <trash directory>] [-n <integer>]"
}

while getopts "xd:t:n:" opt; do
    case $opt in
        d)
            TARGET_DIR="$OPTARG"
            ;;
        t)
            TRASH_DIR="$OPTARG"
            ;;
        x)
            TRASH_DIR=
            ;;
        n)
            NUM_DAYS="$OPTARG"
            ;;
        \?)
            print_usage
            exit 1
            ;;
    esac
done

echo "Target directory is $TARGET_DIR"
echo "Deleting files older than $NUM_DAYS"
if [ -z "$TRASH_DIR" ];  then
    echo "Hard deleting files - not using a Trash directory"
else
    echo "Trash direcotry is $TRASH_DIR"
fi

function create_crontab() {
    echo "# Begin Janitor job"
    echo "0  */6  *  *  * $(pwd)/bin/janitor $1 $2 $3"
    echo "# End Janitor job"
}

function check_crontab() {
    if [[ $1 == *"# Begin Janitor job"* && \
          $1 == *"# End Janitor job"* ]]; then
        return 1
    else
        return 0
    fi
}

# Create crontab
if check_crontab "$(crontab -l 2>/dev/null)"; then
    # Crontab exists but does not already contain ours
    echo "Creating crontab entry."
    entry=$(create_crontab "$TARGET_DIR" "$NUM_DAYS" "$TRASH_DIR")
    (crontab -l 2>/dev/null; [[ $? -eq 0 ]] && echo " " ; echo "$entry") | crontab -
else
    echo "Janitor cronjob already exists. Remove the current job (using crontab -e) and re-run this installation script."
    exit 1
fi

mkdir -p logs

echo "Installation complete."
exit 0
