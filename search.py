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
from Customization import Configuration as C


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

    @staticmethod
    def _matched(patterns, content):
        """ Search for matches """
        for pattern in patterns:
            # ignore case
            if not re.search(r'{}'.format(pattern), content, re.I):
                return False
        return True

    @classmethod
    def wiki_search(cls, search_terms, dicted_files):
        matched_list = []
        for f in dicted_files:
            if search_terms[0] in f['title']:
                matched_list.append(f)
        return matched_list

    @classmethod
    def notes_search(cls, search_terms, dicted_files):
        """ Get a list of matched files """
        matched_list = []
        for f in dicted_files:
            if cls._matched(search_terms, f['content']):
                matched_list.append(f)
        return matched_list

    @classmethod
    def tag_search(cls, search_tags, dicted_files):
        matched_list = []
        for f in dicted_files:
            tags = []
            match = Note.get_yaml_item('tags', f["content"])
            if match:
                tags.extend(match.strip('[]').split(','))
            if not C.SETTINGS["search_yaml_tag_only"]:
                tags.extend(re.findall(r'\b#(.*?)\b', f['content']), re.I)
            if not tags:
                continue
            else:
                # TODO: handle multi tags
                for t in search_tags:
                    if t in tags:
                        matched_list.append(f)
        return matched_list

    @classmethod
    def both_search(cls, keywords, tags, dicted_files):
        # TODO: alter between `and` and `or`
        matched_list = cls.notes_search(keywords, dicted_files)
        matched_list = cls.tag_search(tags, matched_list)
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
            result = S.wiki_search(keywords, sorted_wiki_list)
        elif mode == "Keywords":
            result = S.notes_search(keywords, sorted_file_list)
        elif mode == "Tags":
            result = S.tag_search(tags, sorted_file_list)
        elif mode == "Both":
            result = S.both_search(keywords, tags, sorted_file_list)
        else:
            result = None
    except Exception as e:
        U.log(e)
        return None
    else:
        I = Items()
        if not result:
            I.add_none_matched_item(query)
        else:
            num = C.SETTINGS["result_nums"] if isinstance(
                C.SETTINGS["result_nums"], int) else 20
            I.add_result_items(result[:num])
        I.write()

if __name__ == "__main__":
    main()
