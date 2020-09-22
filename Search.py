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
        self.file_name = ""
        self.yaml = ""
        self.content = ""
        self.title = ""

    @staticmethod
    def get_yaml_item(item, content):
        match = re.search(
            r'^---.*?\b{}s?: (.*?)\n.*?---'.format(item), content, re.I | re.S)
        return match.group(1) if match is not None else None

    def get_file_title(self, path):
        """ yaml_title > level_one_title > file_name """
        self.path = path
        self.file_name = U.get_file_name(self.path).lower()
        all_text = U.get_file_content(self.path).lower()
        match = re.search(r'(---.*?---)([\s\S]+)', all_text, re.I | re.S)
        if match and len(match.groups()) == 2:
            self.yaml = match.group(1)
            self.content = match.group(2).strip()
        else:
            U.log(self.file_name)
            self.yaml, self.content = "", all_text
        yaml_title = self.get_yaml_item("title", self.yaml)
        level_one_title = re.search(r'^# (\s+)', self.content)
        self.title = yaml_title or level_one_title or self.file_name or ""
        return self.title

    @classmethod
    def get_file_info(cls, path):
        """ get file's info in a dict """
        cls.get_file_title(cls, path)
        folder = path.split("/")[-2] if len(path.split('/'))>2 else "<root>"
        size = U.get_file_meta(cls.path, "st_size")
        ctime_float = U.get_file_meta(cls.path, "st_birthtime")
        mtime_float = U.get_file_meta(cls.path, "st_mtime")
        cdate_string = U.format_date(ctime_float, "%Y-%m-%d")
        mdate_string = U.format_date(mtime_float, "%Y-%m-%d")
        file_infos = {
            'path': cls.path,
            'file_name': cls.file_name,
            'yaml': cls.yaml,
            'content': cls.content,
            'title': cls.title,
            'folder': folder,
            'cdate': cdate_string,
            'mdate': mdate_string,
            'ctime': ctime_float,
            'mtime': mtime_float,
            'size': size,
            'synonyms': cls.get_yaml_item('synonyms', cls.content)
        }
        return file_infos


class Search():
    """ handle all search procblems"""

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
    def title_search(cls, search_terms, dicted_files):
        matched_list = []
        for f in dicted_files:
            if f['title'] in cls.synonyms_search(search_terms):
                matched_list.append(f)
            elif search_terms[0] in f['title']:
                matched_list.append(f)
        return matched_list

    @classmethod
    def and_search(cls, search_terms, dicted_files):
        def _matched(terms, file):
            for term in terms:
                if not re.search(term, file, re.I):
                    return False
            return True

        matched_list = []
        for f in dicted_files:
            if _matched(search_terms, f['content']):
                matched_list.append(f)
        return matched_list

    @classmethod
    def or_search(cls, search_terms, dicted_files):
        def _matched(terms, file):
            for term in terms:
                if re.search(term, file, re.I):
                    return True
            return False

        matched_list = []
        for f in dicted_files:
            if _matched(search_terms, f['content']):
                matched_list.append(f)
        return matched_list

    @classmethod
    def metric_search(cls, metric, keys, dicted_files):
        # Search notes by keys of specific metrics (tag, snippet ...)
        matched_notes = []
        for f in dicted_files:
            has_keys = []
            # Check YAML frontier to get note's assigned metrics
            match = File.get_yaml_item(metric, f["content"])
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
    def synonyms_search(cls, search_terms):
        # Or_Search, TODO: match whole phrase
        synonyms = U.json_load(U.path_join(Config.CONFIG_DIR, 'synonyms.json'))
        out = []
        for k in list(synonyms.keys()):
            for s in synonyms[k]:
                if search_terms[0] in s:
                    out.append(k)
        return out

    @staticmethod
    def markdown_links_search(path, filename=False):
        "Get a list of Markdown links which contained in the file (by given path/filename)"
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
