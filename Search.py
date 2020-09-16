#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------
# Created by Konfido on 2020-07-16
# --------------------------------------


import re

import Config
from Items import Items, Display
from Utils import Utils as U

C = Config.Config().configs


class File():
    def __init__(self):
        self.path = ""
        self.filename = ""
        self.content = ""
        self.title = ""

    def get_file_title(self, path):
        """ yaml_title > level_one_title > file_name """
        self.path = path
        self.file_name = U.get_file_name(self.path).lower()
        self.content = U.get_file_content(self.path).lower()

        yaml_title = U.get_yaml_item("title", self.content)
        level_one_title = re.search(r'^# (\s+)', self.content)
        self.title = yaml_title or level_one_title or self.file_name or ""
        return self.title

    @classmethod
    def get_file_info(cls, path):
        """ get file's info in a dict """
        cls.get_file_title(cls, path)
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
            'size': size,
            'synonyms': U.get_yaml_item('synonyms', cls.content)
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

    @staticmethod
    def show_search_result(query, matched_list):
        items = []
        for m in matched_list:
            items.append({
                "title": m['title'],
                "subtitle": f"{m['mdate']}, (\u2318-Actions, \u21E7-Quicklook)",
                "type": 'file',
                "arg": f'open|{m["path"]}',
                "mods": {
                    "cmd": {
                        "arg": f'show_actions|[{m["path"]}, {query}]',
                        "subtitle": "Press 'Enter' to select your next action"
                    }},
                "quicklookurl": m["path"]
                })
        Display.show(items)

    @classmethod
    def title_search(cls, search_terms, dicted_files):
        matched_list = []
        for f in dicted_files:
            if f['title'] in cls.synonyms_search(search_terms):
                matched_list.append(f)
            elif search_terms[0] in f['title']:
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
    def metric_search(cls, metric, keys, dicted_files):
        # Search notes by keys of specific metrics (tag, snippet ...)
        matched_notes = []
        for f in dicted_files:
            has_keys = []
            # Check YAML frontier to get note's assigned metrics
            match = U.get_yaml_item(metric, f["content"])
            if match:
                has_keys.extend(match.strip('[]').split(', '))
            # Check content to get note's specific metrics
            if metric in ["tag","tags"] and not C["search_tag_yaml_only"]:
                has_keys.extend(re.findall(r'\b#(.*?)\b', f['content'], re.I))
            elif metric is "language" and not C["search_snippet_yaml_only"]:
                has_keys.extend(re.findall(r'```(\S+)', f['content'], re.I))

            if not has_keys:
                continue
            else:
                for k in keys:
                    if k in has_keys:
                        matched_notes.append(f)
        return matched_notes

    @classmethod
    def both_search(cls, keywords, metrics, dicted_files):
        "metrics: [metric, keys]"
        metric, keys = metrics
        matched_list = cls.notes_search(keywords, dicted_files)
        matched_list = cls.metric_search(metric, keys, matched_list)
        return matched_list

    @classmethod
    def synonyms_search(cls, search_terms):
        synonyms = U.json_load(U.path_join(Config.CONFIG_DIR, 'synonyms.json'))
        out = []
        for k in list(synonyms.keys()):
            for s in synonyms[k]:
                # TODO:
                if search_terms[0] in s:
                    out.append(k)
        return out

    @staticmethod
    def markdown_links_search(path, filename=False):
        "Query dict with path/filename to get a link_list contained in this file"
        abs_path = path if not filename else U.get_abspath(path, relative_path=True)
        content = U.get_file_content(abs_path)
        # exclude images link: ![]() and url: [](https://)
        links_info = re.findall(
            r'(?<!!)(\[(.*?)\]\(((?!http).*?md)\))', content)
        link_list = [l[2] for l in links_info]
        return link_list

    @staticmethod
    def backlinks_search(filename):
        "Query dict with path/filename to get a backlink list"
        # TODO: decouple with synonyms_search()
        # Only query the dict with filename
        filename = U.get_file_name(filename, with_ext=True)
        backlinks = U.json_load(U.path_join(Config.CONFIG_DIR, 'backlinks.json'))
        matched_list = backlinks[filename] if backlinks.__contains__(filename) else []
        return matched_list
