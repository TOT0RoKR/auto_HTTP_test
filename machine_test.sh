#!/bin/sh
HOMEDIR="/home/wyldecat"
MAINDIR="/home/wyldecat/machinetest"

# sh -c "$HOMEDIR/Fastset-no-option.sh" # sysctl, environment set
# sh -c "$MAINDIR 9"
python3 master.py

