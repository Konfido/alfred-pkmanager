#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 16th 2020
# ------------------------------------------------


import sys
import json
import os
import re
from PKM import Items
from PKM import Utils as U
# from PKM import Search as S
from PKM import Note
# from Customization import SETTINGS


class Search():
    # def __init__(self):
    #     self.paths = []
    #     self.file_infos = []

    @staticmethod
    def _get_all_files(env_paths):
        file_paths_list = []
        # support multi note paths
        for path in env_paths:
            # support subfolders
            for root, dirs, files in os.walk(path):
                for name in files:
                    if name.endswith(".md"):
                        file_paths_list.append(os.path.join(root, name))
        if not file_paths_list:
            U.show("No valid notes, please input file's name to create one.")
            exit()
        return file_paths_list

    @classmethod
    def get_sorted_files(cls, paths, reverse=True):
        """ Get all files sorted by modification time in reserve """
        matched_list = list()
        for path in cls._get_all_files(paths):
            matched_list.append(Note.get_file_info(path))
        sorted_files = sorted(
            matched_list, key=lambda k: k['mtime'], reverse=reverse)
        return sorted_files

    @classmethod
    def show_none_matched(cls, query):
        cls = Items()
        cls.addItem({
            "title": "Nothing found...",
            "subtitle": "Do you want to create a new note with title \"{0}\"?".format(
                query),
            "arg": query
        })
        cls.write()

    @classmethod
    def show_result_items(cls, dicted_files):
        cls = Items()
        for f in dicted_files:
            cls.addItem({
                "title": f['title'],
                "subtitle": u"Modified: {0}, Created: {1}, ({2} Actions, {3} Quicklook)".format(
                    f['mdate'], f['cdate'], u'\u2318', u'\u21E7'),
                "type": 'file',
                "arg": f['path']
            })
        cls.write()

    @staticmethod
    def _matched(patterns, content):
        """ Search for matches """
        for pattern in patterns:
            if not re.search(r'{}'.format(pattern), content, re.I):
                return False
        return True

    @classmethod
    def notes_search(cls, search_terms, dicted_files):
        """ Get a list of matched files """
        matched_list = []
        for f in dicted_files:
            if cls._matched(search_terms, f['content']):
                matched_list.append(f)
        return matched_list


def main():
    query = U.get_query()

    if not U.get_env_varibles():
        return None

    # Load env variables
    wiki_path, notes_path = U.get_env_varibles()
    # Parse search input
    mode, keywords, tags = U.get_parsed_arg()

    S = Search()
    sorted_wiki_list = S.get_sorted_files(wiki_path)
    sorted_file_list = S.get_sorted_files(notes_path)
    try:
        if mode == "Recent":
            result = sorted_file_list
        elif mode == "WIKI":
            result = S.notes_search(keywords, sorted_wiki_list)
        elif mode == "Keywords":
            result = S.notes_search(keywords, sorted_file_list)
        elif mode == "Both":
            pass
        elif mode == "Tags":
            pass
        else:
            result = None
    except Exception as e:
        U.log(e)
        return None
    else:
        if not result:
            S.show_none_matched(query)
        else:
            S.show_result_items(result)

if __name__ == "__main__":
    main()
