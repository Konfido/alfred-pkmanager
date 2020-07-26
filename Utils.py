#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 26th 2020
# ------------------------------------------------

import os
import sys
import time
import re

class Utils():

    @staticmethod
    def get_env(var):
        """ Reads environment variable """
        return os.getenv(var) if os.getenv(var) is not None else str()

    @staticmethod
    def get_abspath(path):
        return os.path.expanduser(path)

    @staticmethod
    def get_file_meta(path, key):
        metas = os.stat(path)
        try:
            return metas.__getattribute__(key)
        except AttributeError:
            raise
        return None

    @staticmethod
    def get_file_name(path, with_ext=False):
        """ get file's name from path """
        file = os.path.basename(path)
        if not with_ext:
            file, ext = os.path.splitext(file)
        return file

    @staticmethod
    def get_file_content(path):
        # only process Markdown file
        if str(path).endswith(".md"):
            with open(path, 'r') as f:
                content = f.read()
        else:
            content = str()
        return content

    @staticmethod
    def get_yaml_item(item, content):
        match = re.search(
            r'^---.*?\b{}: (.*?)\n.*?---'.format(item), content, re.I | re.S)
        return match.group(1) if match is not None else None

    @classmethod
    def get_env_varibles(cls):
        """ Check valibility of env variables"""
        for env in ["MARKDOWN_APP", "NOTES_PATH", "WIKI_PATH"]:
            if not cls.get_env(env):
                cls.show(("ERROR: Find empty environt varibles!",
                          "Please check: \"{}\".".format(env)))
                return False
        for path in cls.get_env("NOTES_PATH").split(","):
            if not(os.path.exists(path)):
                cls.show(("ERROR: Find invalid directory!",
                          "Please check \"NOTES_PATH\": {}".format(path)))
                return False
        if not cls.get_env("WIKI_PATH"):
            cls.show(("ERROR: Find invalid directory!",
                      "Please check \"WIKI_PATH\""))
            return False

        notes_path = cls.get_abspath(cls.get_env("NOTES_PATH")).split(",")
        wiki_path = cls.get_abspath(cls.get_env("WIKI_PATH")).split(",")
        return (wiki_path, notes_path)

    @staticmethod
    def get_query():
        return sys.argv[1].lower()

    @classmethod
    def get_parsed_arg(cls):
        # Tring to fetch input string
        query = cls.get_query()
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
                    mode, keywords, tags = "WIKI", [query.strip()], []
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
                cls.show(("Error!", "Having 2 (>=) commas is not allowed!"))
                exit(0)
                mode, keywords, tags = "", [], []
            else:
                cls.show(
                    ("Error!", "Can't parse the input: \'{0}\'".format(query)))
                exit(0)
                mode, keywords, tags = "", [], []

        return mode, keywords, tags

    @staticmethod
    def log(message):
        sys.stderr.write('LOG: {0}\n'.format(message))

    @staticmethod
    def notify(title, text="PKManger"):
        """ Send Notification to mac Notification Center """
        os.system("""osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))

    @classmethod
    def show(cls, *args):
        """ Used under debugging: Send debug message to script filter

        Allowed input format:
            - String/Int/Float/List -> Title
            - Tuple: T[0] -> Title; T[1] -> Subtitle
            - Dict: {"Title": "xx", "Subtitle": "xx"}
        """
        cls = Items()
        for item in args:
            try:
                if isinstance(item, str) or isinstance(item, int) or isinstance(item, float):
                    cls.add_item({"title": item})
                    continue
                if isinstance(item, list):
                    for i in item:
                        cls.add_item({"title": i})
                    continue
                elif isinstance(item, tuple):
                    title = item[0]
                    subtitle = item[1]
                elif isinstance(item, dict) and item.has_key("title"):
                    title = item["title"]
                    subtitle = item["subtitle"] if item.has_key(
                        "subtitle") else ""
                else:
                    cls.add_item({"title": "Error!",
                                  "subtitle": "Filter {}".format(item)})
                    continue

                cls.add_item({"title": title,
                              "subtitle": subtitle})
            except Exception as e:
                cls.add_item({"title": "Exception!",
                              "subtitle": e})
        cls.write()

    @staticmethod
    def get_now(fmt="%Y-%m-%d %H:%M:%S"):
        """ Get formated current date&time string """
        now = datetime.datetime.now()
        return now.strftime(fmt)

    @staticmethod
    def format_date(float_date, fmt="%Y-%m-%d %H:%M:%S"):
        """ float time to string """
        return time.strftime(fmt, time.localtime(float_date))

    @staticmethod
    def str_replace(string, replace_map):
        for r in replace_map.keys():
            string = string.replace(r, replace_map[r])
        return string
