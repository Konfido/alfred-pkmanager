#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 27th 2020
# ------------------------------------------------


from Config import Config
from Items import Display
from Utils import Utils as U


# get variable from env
# the query passing through is none to keep input box clean
if U.get_env('second_1'):
    option = U.get_env('second_1')
    arg = U.get_env('second_2')
else:
    option = U.get_env('next_1')
    arg = U.get_env('next_2')

if option == "Next":
    path, query = U.literal_eval(arg)
    file_name = U.get_file_name(path)
    m_path, m_type = "icon", "image"

    Display.show(
        {
            "title": "Back",
            "subtitle": "Back to Search with query: {}".format(query),
            # "arg": f"back|{query}",
            "arg": "{}|{}".format("back", query),
            # "icon": "icons/back.png",
        },
        {
            "title": "Markdown Link",
            "subtitle": "Copy MD Link for \"{}\" to the Clipboard".format(file_name),
            "arg": "{}|[{}]({})".format("link", file_name, path),
            # "icon": "icons/link.png",
        },
        {
            "title": "Delete Note",
            "subtitle": "Delete \"{}\". This action cannot be undone!".format(file_name),
            "arg": "{}|{}".format("delete", [path, file_name]),
            # "icon": "icons/delete.png",
        }
    )

elif option == "select_config":
    C = Config().configs
    _tag = str(not C["search_yaml_tag_only"])
    _todo = "newest" if C["todo_order"] == "oldest" else "newest"

    Display.show(
        {
            "title": "Only search the tags in YAML frontier",
            "subtitle": "Change to \"{}\"".format(_tag),
            "arg": "{}|{}".format("swap_config", "search_yaml_tag_only")
        },
        {
            "title": "Show {} TODOs in the top".format(C["todo_order"]),
            "subtitle": "Change to \"{}\"".format(_todo),
            "arg": "{}|{}".format("swap_config", "todo_order")
        },
        {
            "title": "Number of reserved searching results".format(),
            "subtitle": str(C["result_nums"]),
            "arg": "{}|{}".format("receive_config", "result_nums")
        },
        {
            "title": "Date format used in templates",
            "subtitle": "{}".format(C["date_format"]),
            "arg": "{}|{}".format("receive_config", "date_format")
        },
        {
            "title": "Path to your new created Note",
            "subtitle": "{}".format(C["new_note_path"]),
            "arg": "{}|{}".format("receive_config", "new_note_path")
        },
        {
            "title": "Path to your new created Wiki",
            "subtitle": "{}".format(C["new_wiki_path"]),
            "arg": "{}|{}".format("receive_config", "new_wiki_path")
        },
        {
            "title": "Path to your new created TODO",
            "subtitle": "{}".format(C["new_todo_path"]),
            "arg": "{}|{}".format("receive_config", "new_todo_path")
        },
        {
            "title": "Path to your new created Journal",
            "subtitle": "{}".format(C["new_journal_path"]),
            "arg": "{}|{}".format("receive_config", "new_journal_path")
        },
    )

elif option == "receive_config":
    try:
        value = U.get_query()
    except:
        value = ""

    Display.show(
        {
            "title": "Input a new value of your \"{}\"".format(arg),
            "subtitle": "Press \"Enter\" to confirm",
            "arg": "{}|{}".format("set_config", [arg, value])
        }
    )
