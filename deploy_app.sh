#!/usr/bin/env bash

set -e

# The script can be run from anywhere inside repository. It uses application module path
# to set up for GAE deployment
if [ "$#" -lt 1 ]; then
    echo "Missing the required name of application module which will serve version" >&2
    echo $0 moduld_name \(app.yaml\)
    exit 1
fi

APP_DIR=$1
if [ ! -d "$APP_DIR" ]; then
    echo "$APP_DIR does not exist" >&2
    exit 1
fi

# one level up of $APP_DIR is the working dir
echo "Generating source_tip.txt in $APP_DIR"
cd $APP_DIR/..
pwd

intree=$(git rev-parse --is-inside-work-tree)
if [ $intree != 'true' ]; then
    echo "Not in a git repository" >&2
    exit 1
fi

config=${2:-app.yaml}

GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
GIT_HASH=$(git rev-parse HEAD)
GIT_DIRTY=$(git diff --quiet || echo '-dirty')
APP_DIR=$(basename $APP_DIR)
echo "${GIT_BRANCH}:${GIT_HASH}${GIT_DIRTY}">$APP_DIR/source_tip.txt

echo "Set source code version to: `cat $APP_DIR/source_tip.txt`"

echo
echo "If you choose yes, this command will run"
echo "gcloud -q app deploy $config"
echo

# https://stackoverflow.com/questions/226703/how-do-i-prompt-for-yes-no-cancel-input-in-a-linux-shell-script/27875395#27875395
while true; do
    read -p "Do you want to deploy to GAE without verifying?" yn
    case $yn in
        [Yy]* ) gcloud -q app deploy $config; exit;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
