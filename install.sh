#!/usr/bin/env bash

# Symlink janitor.sh to /usr/local/bin/janitor
if [ ! -L $HOME/.janitor.sh ]; then
    echo "Creating symlinks."
    ln -s $(pwd)/janitor.sh $HOME/.janitor.sh 
fi

# Create crontab
CRONTAB="$(crontab -l 2>/dev/null)"
if [ $? -ne 0 ]; then
    # No existing crontab
    echo "Creating crontab entry."
    crontab crontab
elif [[ $CRONTAB != *"$(cat crontab)" ]]; then
    # Crontab exists but does not already contain ours
    echo "Creating crontab entry."
    (crontab -l ; cat crontab) | crontab -
fi

mkdir -p logs

echo "Installation complete."
exit 0
