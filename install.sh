#!/usr/bin/env bash

TARGET_DIR=$HOME/Downloads
NUM_DAYS=30
TRASH_DIR=$HOME/.Trash

while getopts "d:t:n:" opt; do
    case $opt in
        d)
            TARGET_DIR="$OPTARG"
            ;;
        t)
            TRASH_DIR="$OPTARG"
            ;;
        n)
            NUM_DAYS="$OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done

echo "Target directory is $TARGET_DIR"
echo "Deleting files older than $NUM_DAYS"
echo "Trash direcotry is $TRASH_DIR"

function create_crontab() {
    echo " "
    echo "# Begin Janitor job"
    echo "0  */6  *  *  * $(pwd)/bin/janitor $1 $2 $3"
    echo "# End Janitor job"
}

CURRENT_CRONTAB="$(crontab -l 2>/dev/null)"
function check_crontab() {
    if [[ $CURRENT_CRONTAB == *"# Begin Janitor job"* && \
          $CURRENT_CRONTAB == *"# End Janitor job"* ]]; then
        return 1
    else
        return 0
    fi
}


# Create crontab
if [ $? -ne 0 ]; then
    # No existing crontab
    echo "Creating crontab entry."
    crontab crontab
else
    if check_crontab; then
        CRONTAB=$(create_crontab "$TARGET_DIR" "$NUM_DAYS" "$TRASH_DIR")
        # Crontab exists but does not already contain ours
        echo "Creating crontab entry."
        (crontab -l ; echo "$CRONTAB") | crontab -
    else
        echo "Janitor cronjob already exists. Remove the current job (using crontab -e) and re-run this installation script."
        exit 1
    fi
fi

mkdir -p logs

echo "Installation complete."
exit 0
