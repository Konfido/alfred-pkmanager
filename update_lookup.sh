#!/bin/bash
# --------------------------------------
# Created by Konfido on 2020-09-25
# --------------------------------------


# Add env to use `fswatch`
PATH=$PATH:/usr/local/bin/


realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

notify() {
    osascript -e "display notification \"$1\" with title \"$2\""
}

data_dir="$alfred_workflow_data"
logfile="${data_dir}/log.txt"
date=$(date +"%Y-%m-%d %H:%M:%S")
# Convert `files_path` to realpath and romove quotation mark of it
monitor_path=$(realpath $(eval echo $files_path))


if [ "$1" = "Start" ]; then
    echo "$date Start to monitor ..." >> "${logfile}"
    fswatch -rxv0 "${monitor_path}" | while read -d "" event; do
        active_file=$(grep -o "/Users.*md" <<< "$event")
        # Escape Typora's renaming process
        [[ $active_file == *~.md* ]] && exit 0
        case ${event} in
            *"Renamed Updated IsFile"*)
                notify "${event}" Updated
                echo "$date ${event}" >> "${logfile}"
                ;;
            *Created*)
                notify "${event}" Created
                echo "$date ${event}" >> "${logfile}"
                ;;
            *Removed*)
                notify "${event}" Removed
                echo "$date ${event}" >> "${logfile}"
                ;;
            *MovedTo*)
                notify "${event}" Moved
                echo "$date ${event}" >> "${logfile}"
                # Update path's lookup of current note
                ;;
            *)
                echo "$date ${event}" >> "${logfile}"
                ;;
        esac
    done &
elif [ "$1" = "Stop" ]; then
    echo "$date Stop monitoring ..." >> "${logfile}"
    kill $(ps -ef | grep -v "grep" | grep fswatch | grep "${monitor_path}" | awk '{print $2}')
else
    echo "$date Error: $1" >> "${logfile}"
fi