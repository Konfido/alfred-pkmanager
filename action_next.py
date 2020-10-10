#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------
# Created by Konfido on 2020-07-27
# --------------------------------------


import re
import os

import Config
from Items import Display, Items
from Utils import Utils as U
from Search import File as F
from Search import Search as S


inputs = U.get_query()
option = U.get_env('next_1')
arg = U.get_env('next_2')
C = Config.Config().configs


if option == "show_error":
    step, message = arg.strip('[]').split(", ")
    Display.show((f"Error happened in the step of {step}", message))

elif option == "show_actions":
    path, query = arg.strip('[]').split(", ")
    # Get relative path to selected note from current opened note
    filename = U.get_typora_filename()
    if filename:
        start_path = os.path.dirname(U.get_abspath(filename, query_dict=True))
        rel_path = U.get_relpath(path, start_path)
    else:
        rel_path = "Failed. Not found opened note in Typora."

    file_title = F().get_file_title(path)
    m_path, m_type = "icon", "image"

    Display.show(
        {
            "title": "Back ⏎",
            "subtitle": f"Back to Search with: {query}",
            "arg": f"back|{query}",
            # "icon": "icons/back.png",
        },
        {
            "title": "Copy Relative Path",
            "subtitle": f"{rel_path}",
            "arg": f"link|{rel_path}",
        },
        {
            "title": "Copy Markdown Link",
            "subtitle": f"[{file_title}]({path})",
            "arg": f"link|[{file_title}]({path})",
            # "icon": "icons/link.png",
        },
        {
            "title": "Refresh YAML",
            "subtitle": "updated: ...",
            "arg": f'refresh|'
        },
        {
            "title": "Reveal in Finder",
            "subtitle": f"{path}",
            "arg": f"reveal|{path}",
        },
        {
            "title": "Delete",
            "subtitle": f"Move this note to Trash",
            "arg": f"delete|[{path}, {file_title}]",
            # "icon": "icons/delete.png",
        })

elif option == "show_configs":

    Display.show(
        {
            "title": "Configure",
            "subtitle": "Go next and see the details",
            "arg": f"show_editable_configs|"
        },
        {
            "title": "Update Lookups",
            "subtitle": "'synonyms', 'backlinks',  ...",
            "arg": f'update|'
        },
        {
            "title": "Open Config File",
            "subtitle": "Open & Modify a JSON formatted config file",
            "arg": f"open_config_file|{Config.CONFIG_PATH}"
        },
        {
            "title": "Open Templates Folder",
            "subtitle": "Put your Markdown templates files in the folder",
            "arg": f"open_template|{Config.TEMPLATE_DIR}"
        },
        {
            "title": "Reset All Configurations",
            "subtitle": "Configs will be reverted to default. This can't be undone!",
            "arg": f"reset_all_configs|"
        }
    )

elif option == "show_editable_configs":

    _todo = "newest" if C["todo_order"] == "oldest" else "newest"
    _tag = "by the hash(#) mark" if C["search_tag_yaml_only"] else "in YAML frontier"
    _language = "code fences" if C["search_snippet_yaml_only"] else "YAML frontier"
    _scope = "its exclusive folder" if C["search_all_folders"] else "all folders"

    fswatch = os.popen(
        'if [ "$(pgrep fswatch| wc -l)" -eq 0 ] \
            || [[ $(ps -ef|grep -v "grep"|grep fswatch) != *$monitor_path* ]]; \
                then echo 0; else echo 1; fi').read().strip()
    _monitor = "Start" if fswatch == '0' else "Stop"

    items = []
    items.extend([
        # configs - just toggle
        {
            "title": "Toggle Modification Monitoring",
            "subtitle": f"\"{_monitor}\" auto-updating notes\' lookups in the background?",
            "arg": f'auto_update|{_monitor}'
        },
        {
            "title": "Toggle Tags Searching Mode",
            "subtitle": f"Search tags specified \"{_tag}\"?",
            "arg": "swap_config|search_tag_yaml_only"
        },
        {
            "title": "Toggle Snippet Searching Mode",
            "subtitle": f"Search snippet by code's language specified in \"{_language}\"?",
            "arg": "swap_config|search_snippet_yaml_only"
        },
        {
            "title": "Toggle Order of To-dos",
            "subtitle": f"List \"{_todo}\" To-dos in the top?",
            "arg": "swap_config|todo_order"
        },
        {
            "title": "Toggle Search Scope",
            "subtitle": f"Search Snippet/Notes in \"{_scope}\"?",
            "arg": "swap_config|search_all_folders"
        },
    ])

    items.extend([
        # configs - new value needed
        {
            "title": "Number of Reserved Search Results".format(),
            "subtitle": str(C["result_nums"]),
            "arg": "show_receive_config|result_nums"
        },
        {
            "title": "Configurate Weather API Key",
            "subtitle": "Input your your API key. (Press \u2318 to create your free weather API) ",
            "arg": "show_receive_config|weather_api",
            "mods": {
                "cmd": {
                    "arg": "create_weather_api|",
                    "subtitle": "Press \"Enter\" to open signup page (free api up to 1,000,000 calls/month)"
                },
            }
        }
    ])
    for i in C["templates"]:
        items.append({
            "title": f"Desired Path to New {i}",
            "subtitle": C[f"path_to_new_{i}"],
            "arg": f"show_receive_config|path_to_new_{i}"
        })
    Display.show(items)

elif option == "show_receive_config":
    config_key = arg
    config_value = U.get_query()
    subtitle = "Press \"Enter\" to Confirm"
    if config_key == "weather_api":
        subtitle = "Fill in your API key ( Or press \u2318 to create your free weather API)"
        mods = {
            "cmd": {
                "arg": "show_receive_config|weather_api",
                "subtitle": "Press \"Enter\" to open signup page (free api up to 1,000,000 calls/month)"
            },
        }

    Display.show(
        {
            "title": f'Input A New Value of Your "{config_key}"',
            "subtitle": subtitle,
            "arg": f"set_config|[{config_key}, {config_value}]",
            "mods": mods,
        }
    )

else:
    U.notify("Error")
