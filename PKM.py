#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 16th 2020
# ------------------------------------------------


from Customization import SETTINGS
from Items import Items
from Search import File as F
from Search import Search as S
from Utils import Utils as U


def varibles_checked():
    """ Check validity of env variables"""
    for env in ["markdown_app", "notes_path", "wiki_path"]:
        if not U.get_env(env):
            Items().show(("ERROR: Find empty environt varibles!",
                          "Please check: \"{}\".".format(env)))
            return False
    for path in U.get_env("notes_path").split(","):
        if not(U.path_exists(U.get_abspath(path))):
            Items().show(("ERROR: Find invalid directory!",
                          "Please check \"notes_path\": {}".format(path)))
            return False
    if not U.get_env("wiki_path"):
        Items().show(("ERROR: Find invalid directory!",
                      "Please check \"wiki_path\""))
        return False

    return True


def main():
    query = U.get_query()
    notes_path = U.get_abspath(U.get_env("notes_path")).split(",")
    wiki_path = U.get_abspath(U.get_env("wiki_path")).split(",")

    # Get all sorted wikis and notes
    sorted_wiki_list = S.get_sorted_files(wiki_path)
    sorted_file_list = S.get_sorted_files(notes_path)

    # Parse input
    mode, keywords, tags = U.get_parsed_arg()

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
        Items.show(("Error!", "Having 2 (>=) commas is not allowed!"))
        result = []
    else:
        result = []

    # Generate ScriptFilter Output
    if not result:
        Items.show_none_matched(mode, query)
    else:
        num = SETTINGS["result_nums"] if isinstance(
            SETTINGS["result_nums"], int) else 20
        Items.show_matched_result(result[:num])

    return


if __name__ == "__main__":
    if varibles_checked():
        main()
