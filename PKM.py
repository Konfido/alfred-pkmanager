#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  August 6th 2020
# ------------------------------------------------


import re

import Config
from Items import Display, Items
from Search import File as F
from Search import Search as S
from Utils import Utils as U


C = Config.Config().configs

def varibles_checked():
    all_set = True
    # Check validity of Workflow env variables
    for env in ["markdown_app", "files_path", "notes_path"]:
        if not U.get_env(env):
            Display.show(("ERROR: Find empty environt varibles!",
                          f"Please check: \"{env}\"."))
            all_set = False
    for path in U.get_env("files_path").split(","):
        if not(U.path_exists(U.get_abspath(path))):
            Display.show(("ERROR: Find invalid directory!",
                          f"Please check \"files_path\": {path}"))
            all_set = False
    if not U.get_env("notes_path"):
        Display.show(("ERROR: Find invalid directory!",
                      "Please check \"notes_path\""))
        all_set = False

    # Check validity of config file
    if not U.path_exists(Config.CONFIG_DIR):
        U.mkdir(Config.CONFIG_DIR)
    if not U.path_exists(Config.CONFIG_PATH):
        Config.Config.reset_all()
    else:
        try:
            Config.Config._load_all()
        except Exception as e:
            U.output(f'error|[search, {e}]')
            #TODO: reset all config/go check?
            all_set = False

    return all_set

def get_parsed_arg():
    # no string
    if not query.strip():
        mode, args_1, args_2 = "Recent", [], []
    else:
        commas = re.findall('[,，]', query)
        # no comma
        if not commas:
            args = re.findall(r'(\S+)', query)
            # 1 word with no space tail
            if args.__len__() == 1 and query[-1:] != " ":
                mode, args_1, args_2 = "Title", [query.strip()], []
            # 1 word with space tail & >= 2 words
            else:
                mode, args_1, args_2 = "Args_1", args, []
        # 1 comma
        elif commas.__len__() == 1:
            a1string, a2string = re.match(r'(.*)[,，](.*)', query).groups()
            args_1 = [k for k in a1string.split(" ") if k is not ""]
            args_2 = [t for t in a2string.split(" ") if t is not ""]
            if not args_2:
                mode = "Args_1"
            elif not args_1:
                mode = "Args_2"
            else:
                mode = "Both"
        # >= 2 comma
        elif commas.__len__() >= 2:
            mode, args_1, args_2 = "GT2", [], []
        else:
            U.output(f'error|parse_arg')

    return mode, args_1, args_2

def show_notes():
    if not varibles_checked():
        return 0

    # Get all sorted notes
    if C['search_all_folders']:
        sorted_note_list = S.get_sorted_files(Config.FILES_PATH)
    else:
        sorted_note_list = S.get_sorted_files(Config.NOTES_PATH)

    # Parse input
    mode, keywords, tags = get_parsed_arg()

    if mode == "Recent":
        result = sorted_note_list
    elif mode == "Title":
        result = S.title_search(keywords, sorted_note_list)
    elif mode == "Args_1":
        result = S.notes_search(keywords, sorted_note_list)
    elif mode == "Args_2":
        result = S.metric_search("tag", tags, sorted_note_list)
    elif mode == "Both":
        result = S.both_search(keywords, ["tag", tags], sorted_note_list)
    elif mode == "GT2":
        Display.show(("Error!", "Having 2 (>=) commas is not allowed!"))
        exit()

    # Generate ScriptFilter Output
    if result:
        # show matched results
        num = int(C["result_nums"])
        display_matched_result(query, result[:num])
    else:
        # show none matched info
        Display.show({
            "title": "Nothing found ...",
            "subtitle": f'Presh "⌘" to create a new Note with title \"{query}\"',
            "arg": '',
            "mods": {
                "cmd": {
                    "arg": f'new|[Note>{query}]',
                    "subtitle": "Press 'Enter' to confirm creating"}}})

    return

def show_snippets():
    "Input format: `key1 key2, language1 language2`"
    if not varibles_checked():
        return 0

    # Get all sorted snippets
    if not ['search_all_folders']:
        sorted_note_list = S.get_sorted_files(C["path_to_new_Snippet"])
    else:
        all_files = S.get_sorted_files(Config.FILES_PATH)
        # only search notes with code fences
        sorted_note_list = list(filter(lambda x: "```" in x['content'], all_files))

    # Parse input
    mode, keywords, languages = get_parsed_arg()

    if mode == "Recent":
        result = sorted_note_list
    elif mode == "Title":
        result = S.title_search(keywords, sorted_note_list)
    elif mode == "Args_1":
        result = S.notes_search(keywords, sorted_note_list)
    elif mode == "Args_2":
        result = S.metric_search("language", languages, sorted_note_list)
    elif mode == "Both":
        result = S.both_search(keywords, ["language", languages], sorted_note_list)
    elif mode == "GT2":
        Display.show(("Error!", "Having 2 (>=) commas is not allowed!"))
        exit()

    # Generate ScriptFilter Output
    if result:
        # show matched results
        num = int(C["result_nums"])
        display_matched_result(query, result[:num])
    else:
        # show none matched info
        Display.show({
            "title": "Nothing found ..",
            "subtitle": f'Presh "⌘" to create a new Snippet with title \"{query}\"',
            "arg": '',
            "mods": {
                "cmd": {
                    "arg": f'new|[Snippet>{query}]',
                    "subtitle": "Press <Enter> to confirm creating"}}})

    return

def show_markdown_links():
    """Show MarkDown links contained in currently opened file"""
    filename = U.get_typora_filename()
    if filename:
        link_list = S.markdown_links_search(filename, filename=True)
        matched_list = []
        for link in link_list:
            path = U.get_abspath(link, relative_path=True)
            matched_list.append(F.get_file_info(path))
        if not matched_list:
            Display.show({
                "title": "No MarkDown Link is found in the current file.",
                "subtitle": ""
            })
        else:
            display_matched_result(filename, matched_list)
    else:
        Display.show({
            "title": "Error!",
            "subtitle": "No file is opened in Typora."
        })

def show_backlinks():
    filename = U.get_typora_filename()
    if filename:
        link_list = S.backlinks_search(filename)
        matched_list = []
        for link in link_list:
            path = U.get_abspath(link, relative_path=True)
            matched_list.append(F.get_file_info(path))
        if not matched_list:
            Display.show({
                "title": "Not found related Backlinks",
                "subtitle": "No other notes links to current file"
            })
        else:
            display_matched_result(filename, matched_list)
    else:
        Display.show({
            "title": "Error!",
            "subtitle": "No file is opened in Typora."
        })

def display_matched_result(query, matched_list):
    items = []
    for m in matched_list:
        items.append({
            "title": m['title'],
            "subtitle": Config.WF_SHOW_SUBTITLE.format(
                folder=m["folder"],
                mdate=m["mdate"],
            ),
            "type": 'file',
            "arg": f'open|{m["path"]}',
            "mods": {
                "cmd": {
                    "arg": f'show_actions|[{m["path"]}, {query}]',
                    "subtitle": "Press <Enter> to select your next action"
                }},
            "quicklookurl": m["path"]
        })
    Display.show(items)

if __name__ == "__main__":
    query = U.get_query(lower=True)
    search_type = U.get_search_type()

    if search_type == 'normal':
        show_notes()
    elif search_type == 'markdown_links':
        show_markdown_links()
    elif search_type == 'backlinks':
        show_backlinks()
    elif search_type == 'snippet':
        show_snippets()
    else:
        Display.show("Error!")
