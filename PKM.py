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

def main():
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
        result = S.tag_search(tags, sorted_note_list)
    elif mode == "Both":
        result = S.both_search(keywords, tags, sorted_note_list)
    elif mode == "GT2":
        Display.show(("Error!", "Having 2 (>=) commas is not allowed!"))
        exit()

    # Generate ScriptFilter Output
    if result:
        # show matched results
        num = int(C["result_nums"])
        S.show_search_result(query, result[:num])
    else:
        # show none matched info
        genre = "wiki" if mode == "Wiki" else "note"
        Display.show({
            "title": "Nothing found ..",
            "subtitle": f'Presh "\u2318" to create a new \"{genre}\" with title \"{query}\"',
            "arg": '',
            "mods": {
                "cmd": {
                    "arg": f'new|[{genre}, {query}]',
                    "subtitle": "Press 'Enter' to complete"}}})

    return

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

def search_snippets():
    if C['search_all_folders']:
        sorted_files = []
    else:
        sorted_files = []

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
            S.show_search_result(filename, matched_list)
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
            S.show_search_result(filename, matched_list)
    else:
        Display.show({
            "title": "Error!",
            "subtitle": "No file is opened in Typora."
        })


if __name__ == "__main__":
    query = U.get_query(lower=True)
    search_type = U.get_search_type()

    if search_type == 'normal':
        main()
    elif search_type == 'markdown_links':
        show_markdown_links()
    elif search_type == 'backlinks':
        show_backlinks()
    else:
        Display.show("Error!")
