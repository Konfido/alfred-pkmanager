#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 16th 2020
# ------------------------------------------------


import re

from Config import Config as C
from Items import Items
from Utils import Utils as U


class File():
    def __init__(self, path):
        self.path = path
        self.file_name = U.get_file_name(self.path).lower()
        self.content = U.get_file_content(self.path).lower()
        self.title = self._get_file_title(self).lower()

    def _get_file_title(self):
        """ yaml_title > level_one_title > file_name """
        yaml_title = U.get_yaml_item("title", self.content)
        level_one_title = re.search(r'^# (\s+)', self.content)
        title = yaml_title or level_one_title or self.file_name or ""
        return title

    @classmethod
    def get_file_info(cls, path):
        """ get file's info in a dict """
        cls.__init__(cls, path)
        size = U.get_file_meta(cls.path, "st_size")
        ctime_float = U.get_file_meta(cls.path, "st_birthtime")
        mtime_float = U.get_file_meta(cls.path, "st_mtime")
        cdate_string = U.format_date(ctime_float, "%Y-%m-%d")
        mdate_string = U.format_date(mtime_float, "%Y-%m-%d")
        file_infos = {
            'path': cls.path,
            'file_name': cls.file_name,
            'content': cls.content,
            'title': cls.title,
            'cdate': cdate_string,
            'mdate': mdate_string,
            'ctime': ctime_float,
            'mtime': mtime_float,
            'size': size
        }
        return file_infos


class Search():
    """ handle all search procblems"""

    @staticmethod
    def _matched(patterns, content):
        """ Search for matches """
        for pattern in patterns:
            # ignore case
            if not re.search(r'{}'.format(pattern), content, re.I):
                return False
        return True

    @classmethod
    def get_sorted_files(cls, paths, reverse=True):
        """ Get all files sorted by modification time in reserve """
        all_files = U.get_all_files_path(paths)
        if not all_files:
            return None
        else:
            matched_list = list()
            for path in all_files:
                matched_list.append(File.get_file_info(path))
            sorted_files = sorted(
                matched_list, key=lambda k: k['mtime'], reverse=reverse)
            return sorted_files

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
            match = U.get_yaml_item('tags', f["content"])
            if match:
                tags.extend(match.strip('[]').split(','))
            if not C().configs["search_yaml_tag_only"]:
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
