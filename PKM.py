#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  August 6th 2020
# ------------------------------------------------


import re

from Config import Config as C
from Items import Display, Items
from Search import File as F
from Search import Search as S
from Utils import Utils as U


def main():
    if not varibles_checked():
        return 0

    notes_path = U.get_abspath(U.get_env("notes_path")).split(",")
    wiki_path = U.get_abspath(U.get_env("wiki_path")).split(",")

    # Get all sorted wikis and notes
    sorted_wiki_list = S.get_sorted_files(wiki_path)
    sorted_file_list = S.get_sorted_files(notes_path)

    # Parse input
    mode, keywords, tags = get_parsed_arg()

    if mode == "Recent":
        result = sorted_file_list
    elif mode == "Wiki":
        result = S.wiki_search(keywords, sorted_wiki_list)
    elif mode == "Keywords":
        result = S.notes_search(keywords, sorted_file_list)
    elif mode == "Tags":
        result = S.tag_search(tags, sorted_file_list)
    elif mode == "Both":
        result = S.both_search(keywords, tags, sorted_file_list)
    elif mode == "GT2":
        Display.show(("Error!", "Having 2 (>=) commas is not allowed!"))
        exit()

    # Generate ScriptFilter Output
    if result:
        # show matched results
        num = int(C().configs["result_nums"])
        items = []
        for r in result[:num]:
            items.append({
                "title": r['title'],
                "subtitle": f"{r['mdate']}, ('\u2318' Actions, '\u21E7' Quicklook)",
                "type": 'file',
                "arg": f'open|{r["path"]}',
                "mods": {
                    "cmd": {
                        "arg": f'show_actions|[{r["path"]}, {query}]',
                        "subtitle": "Press 'Enter' to select your next action"
                    }}})
        Display.show(items)
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
    for env in ["markdown_app", "notes_path", "wiki_path"]:
        if not U.get_env(env):
            Display.show(("ERROR: Find empty environt varibles!",
                          f"Please check: \"{env}\"."))
            all_set = False
    for path in U.get_env("notes_path").split(","):
        if not(U.path_exists(U.get_abspath(path))):
            Display.show(("ERROR: Find invalid directory!",
                          f"Please check \"notes_path\": {path}"))
            all_set = False
    if not U.get_env("wiki_path"):
        Display.show(("ERROR: Find invalid directory!",
                      "Please check \"wiki_path\""))
        all_set = False

    # Check validity of config file
    if not U.path_exists(config_dir):
        U.mkdir(config_dir)
    if not U.path_exists(config_path):
        C.reset_all()
    else:
        try:
            C._load_all()
        except Exception as e:
            U.output(f'error|[search, {e}]')
            #TODO: reset all config/go check?
            all_set = False

    return all_set

def get_parsed_arg():
    # no string
    if not query.strip():
        mode, keywords, tags = "Recent", [], []
    else:
        commas = re.findall('[,，]', query)
        # no comma
        if not commas:
            keys = re.findall(r'(\S+)', query)
            # 1 word with no space tail
            if keys.__len__() == 1 and query[-1:] != " ":
                mode, keywords, tags = "Wiki", [query.strip()], []
            # 1 word with space tail & >= 2 words
            else:
                mode, keywords, tags = "Keywords", keys, []
        # 1 comma
        elif commas.__len__() == 1:
            kstring, tstring = re.match(r'(.*)[,，](.*)', query).groups()
            keywords = [k for k in kstring.split(" ") if k is not ""]
            tags = [t for t in tstring.split(" ") if t is not ""]
            if not tags:
                mode = "Keywords"
            elif not keywords:
                mode = "Tags"
            else:
                mode = "Both"
        # >= 2 comma
        elif commas.__len__() >= 2:
            mode, keywords, tags = "GT2", [], []
        else:
            U.output(f'error|parse_arg')

    return mode, keywords, tags


if __name__ == "__main__":
    query = U.get_query()
    config_dir = U.get_env("alfred_workflow_data")
    config_path = U.path_join(config_dir, "config.json")

    main()
