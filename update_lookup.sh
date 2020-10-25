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
    local event=$1
    local title=$2
    time=$(date +"%Y-%m-%d %H:%M:%S")
    osascript -e "display notification \"${event}\" with title \"${title}\""
    echo "$time ${event}" >> "${logfile}"
}

data_dir="$alfred_workflow_data"
logfile="${data_dir}/log.txt"
# Convert `files_path` to realpath and romove quotation mark of it
monitor_path=$(realpath $(eval echo $files_path))


if [ "$1" = "Start" ]; then
    notify "Start to monitor modification." "PKManger"
    fswatch -rxv0 "${monitor_path}" | while read -d "" event; do
        # Escape .DS_Store and Typora's renaming process
        event=$(echo "$event"|grep -v "DS_Store"|grep -v "~.md")
        active_file=$(echo "$event"|grep -o "/Users.*md")
        case ${event} in
            *Created*)
                python3 -c "from action_fast import update_paths_lookup; update_paths_lookup(\"$active_file\")"
                notify "${event}" Created
                ;;
            *Removed*)
                python3 -c "from action_fast import update_paths_lookup; update_paths_lookup(\"$active_file\", type=\"Removed\")"
                notify "${event}" Removed
                ;;
            *MovedTo*)
                # TODO: Handle file's moving
                notify "${event}" Moved
                ;;
            *Updated*)
                python3 -c "from action_fast import update_synonyms_lookup, update_backlinks_lookup; update_synonyms_lookup(\"$active_file\"); update_backlinks_lookup(\"$active_file\")"
                # notify "${event}" Updated
                ;;
            *)
                echo "$(date +"%Y-%m-%d %H:%M:%S") ${event}" >> "${logfile}"
                ;;
        esac
    done &
elif [ "$1" = "Stop" ]; then
    notify "Stop monitoring modification." "PKManger"
    kill $(ps -ef | grep -v "grep" | grep fswatch | grep "${monitor_path}" | awk '{print $2}')
else
    notify "Error! $1" "PKManger"
fi