#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------
# Created by Konfido on 2020-07-27
# --------------------------------------


import re

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
    file_title = F().get_file_title(path)
    m_path, m_type = "icon", "image"

    Display.show(
        {
            "title": "Back",
            "subtitle": f"Back to Search with: {query}",
            "arg": f"back|{query}",
            # "icon": "icons/back.png",
        },
        {
            "title": "Copy Markdown Link",
            "subtitle": f"Copy MD Link for \"{file_title}\" to the Clipboard",
            "arg": f"link|[{file_title}]({path})",
            # "icon": "icons/link.png",
        },
        {
            "title": "Refresh YAML",
            "subtitle": "'updated time', 'synonyms'",
            "arg": f'refresh|'
        },
        {
            "title": "Delete Note",
            "subtitle": f"delete \"{file_title}\". This action cannot be undone!",
            "arg": f"delete|[{path}, {file_title}]",
            # "icon": "icons/delete.png",
        })

elif option == "show_configs":

    Display.show(
        {
            "title": "Set configurations",
            "subtitle": "Go next and see the details",
            "arg": f"show_editable_configs|"
        },
        {
            "title": "Refresh YAML",
            "subtitle": "'updated time', 'synonyms'",
            "arg": f'refresh|'
        },
        {
            "title": "Open config file",
            "subtitle": "Open & Modify a JSON formatted config file",
            "arg": f"open_config_file|{Config.CONFIG_PATH}"
        },
        {
            "title": "Open templates folder",
            "subtitle": "Put your Markdown templates files in the folder",
            "arg": f"open_template|{Config.TEMPLATE_DIR}"
        },
        {
            "title": "Reset all configurations",
            "subtitle": "Configs will be reverted to default. This can't be undone!",
            "arg": f"reset_all_configs|"
        }
    )

elif option == "show_editable_configs":
    _tag = str(not C["search_tag_yaml_only"])
    _todo = "newest" if C["todo_order"] == "oldest" else "newest"

    items = []
    # configs - just toggle
    items.extend([
        {
            "title": "Only search the tags in YAML frontier",
            "subtitle": "Change to \"{}\"".format(_tag),
            "arg": "swap_config|search_tag_yaml_only"
        },
        {
            "title": "Show {} TODOs in the top".format(C["todo_order"]),
            "subtitle": "List \"{}\" TODOs in the top?".format(_todo),
            "arg": "swap_config|todo_order"
        },
    ])
    # configs - new value needed
    items.extend([
        {
            "title": "Number of reserved searching results".format(),
            "subtitle": str(C["result_nums"]),
            "arg": "show_receive_config|result_nums"
        },
        {
            "title": "Configure weather API key",
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
            "title": f"Desired path to new {i}",
            "subtitle": C[f"path_to_new_{i}"],
            "arg": f"show_receive_config|path_to_new_{i}"
        })
    Display.show(items)

elif option == "show_receive_config":
    config_key = arg
    config_value = U.get_query()
    subtitle = "Press \"Enter\" to confirm"
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
            "title": f'Input a new value of your "{config_key}"',
            "subtitle": subtitle,
            "arg": f"set_config|[{config_key}, {config_value}]",
            "mods": mods,
        }
    )

else:
    U.notify("Error")
