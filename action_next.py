#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 27th 2020
# ------------------------------------------------


import re

import Config as C
from Items import Display, Items
from Utils import Utils as U
from Search import File as F
from Search import Search as S


inputs = U.get_query()
option = U.get_env('next_1')
arg = U.get_env('next_2')


if option == "show_error":
    step, message = arg.strip('[]').split(", ")
    Display.show((f"Error happened in the step of {step}", message))

elif option == "show_actions":
    path, query = arg.strip('[]').split(", ")
    file_name = U.get_file_name(path)
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
            "subtitle": f"Copy MD Link for \"{file_name}\" to the Clipboard",
            "arg": f"link|[{file_name}]({path})",
            # "icon": "icons/link.png",
        },
        {
            "title": "Refresh YAML",
            "subtitle": "'updated time', 'synonyms'",
            "arg": f'refresh|'
        },
        {
            "title": "Delete Note",
            "subtitle": f"delete \"{file_name}\". This action cannot be undone!",
            "arg": f"delete|[{path}, {file_name}]",
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
            "arg": f"open_config_file|{C.CONFIG_PATH}"
        },
        {
            "title": "Open templates folder",
            "subtitle": "Put your Markdown templates files in the folder",
            "arg": f"open_template|{C.TEMPLATE_DIR}"
        },
        {
            "title": "Reset all configurations",
            "subtitle": "Configs will be reverted to default. This can't be undone!",
            "arg": f"reset_all_configs|"
        }
    )

elif option == "show_editable_configs":
    C = C.Config().configs
    _tag = str(not C["search_yaml_tag_only"])
    _todo = "newest" if C["todo_order"] == "oldest" else "newest"

    items = []
    items.extend([
        {
            "title": "Only search the tags in YAML frontier",
            "subtitle": "Change to \"{}\"".format(_tag),
            "arg": "swap_config|search_yaml_tag_only"
        },
        {
            "title": "Show {} TODOs in the top".format(C["todo_order"]),
            "subtitle": "List \"{}\" TODOs in the top?".format(_todo),
            "arg": "swap_config|todo_order"
        },
        {
            "title": "Number of reserved searching results".format(),
            "subtitle": str(C["result_nums"]),
            "arg": "show_receive_config|result_nums"
        },
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

    Display.show(
        {
            "title": f'Input a new value of your "{config_key}"',
            "subtitle": "Press \"Enter\" to confirm",
            "arg": f"set_config|[{config_key}, {config_value}]"
        }
    )

else:
    U.notify("Error")
