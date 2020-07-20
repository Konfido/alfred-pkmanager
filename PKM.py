#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 16th 2020
# ------------------------------------------------


import datetime
import json
import os
import re
import sys
import time
import urllib
from collections import Counter, OrderedDict
from plistlib import readPlist, writePlist
from unicodedata import normalize


class Items(object):
    """ To generate Script Filter item """

    def __init__(self):
        self.items = []

    def addItem(self, item):
        """ An item example:
        {   "title": str
            "subtitle": str
            "arg":
            "type":
            "icon": { "type": ""|"image"
                      "path": "icons/hashtag.png" }}
        """
        self.items.append(item)

    def getItems(self, response_type="json"):
        """ get the final items of the script filter output """
        if response_type not in {"json", "dict"}:
            raise ValueError("Type must be in: %s" % {"json", "dict"})

        out = {"items": self.items}

        if response_type == "dict":
            return out
        elif response_type == "json":
            return json.dumps(out)

    def write(self, response_type='json'):
        """ Generate Script Filter Output """
        output = self.getItems(response_type=response_type)
        sys.stdout.write(output)


class Utils(object):

    @staticmethod
    def get_env(var):
        """ Reads environment variable """
        return os.getenv(var) if os.getenv(var) is not None else str()

    @classmethod
    def checked_env_varibles(cls):
        for env in ["MARKDOWN_APP","NOTES_PATH"]:
            if not cls.get_env(env):
                cls.show(
                    (   "ERROR: Find empty environt varibles!",
                        "Please check: \"{}\".".format(env) ))
                # exit(0)
                return False
            else:
                for path in cls.get_env("NOTES_PATH").split(","):
                    if not(os.path.exists(path)):
                        cls.show(
                            (   "ERROR: Find invalid directory!",
                                "Please check \"NOTES_PATH\": {}".format(path)))
                        return False
        return True

    @classmethod
    def get_parsed_arg(cls):
        # Tring to fetch input string
        query = sys.argv[1]
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
                    mode, keywords, tags = "Nodes", [query.strip()], []
                # 1 word with space tail & >= 2 words
                else:
                    mode, keywords, tags = "Keywords", keys, []
            # 1 comma
            elif commas.__len__() == 1:
                kstring, tstring = re.match(r'(.*)[,，](.*)', query).groups()
                keywords = [ k for k in kstring.split(" ") if k is not "" ]
                tags = [ t for t in tstring.split(" ") if t is not "" ]
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
                cls.show(("Error!", "Can't parse the input: \'{0}\'".format(query)))
                exit(0)
                mode, keywords, tags = "", [], []

        return mode, keywords, tags

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
            if isinstance(item, list):
                for i in item:
                    cls.addItem({"title": i})
                continue
            if isinstance(item, str) or isinstance(item, int) or isinstance(item, float):
                cls.addItem({"title":item})
                continue
            elif isinstance(item, tuple):
                title = item[0]
                subtitle = item[1]
            elif isinstance(item, dict) and item.has_key("title"):
                title = item["title"]
                subtitle = item["subtitle"] if item.has_key("subtitle") else ""
            else:
                cls.addItem({
                    "title": "Error!",
                    "subtitle": "Filtering {} ...".format(item)})
                continue

            cls.addItem({
                "title": title,
                "subtitle": subtitle
            })

        cls.write()
