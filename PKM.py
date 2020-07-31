#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 16th 2020
# ------------------------------------------------


from Customization import Config as C
from Items import Items, Display
from Search import File as F
from Search import Search as S
from Utils import Utils as U


def get_parsed_arg():
    # Tring to fetch input string
    query = U.get_query()
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
            U.log(
                ("Error!", "Can't parse the input: \'{0}\'".format(query)))
            raise

    return mode, keywords, tags


def main():
    if not C.varibles_checked():
        return 0

    query = U.get_query()
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
        result = []
    else:
        result = []

    # Generate ScriptFilter Output
    if not result:
        Display.none_matched(mode, query)
    else:
        num = int(C().configs["result_nums"])
        Display.matched_result(result[:num], query)

    return


if __name__ == "__main__":
    main()
