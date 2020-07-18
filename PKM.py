#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 16th 2020
# ------------------------------------------------


import json
import os
import sys
import time
from plistlib import readPlist, writePlist
import re

class Items(object):
    """ To generate Script Filter object """

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
    def getEnv(var):
        """ Reads environment variable """
        return os.getenv(var) if os.getenv(var) is not None else str()

    @staticmethod
    def getArgv(i):
        """ Fetch input string """
        try:
            return sys.argv[i]
        except IndexError:
            return str()

    @classmethod
    def parsedArg(cls):
        query = cls.getArgv(1)
        # no string
        if not query.strip():
            mode, keywords, tags = "Recent", [], []
        # no comma
        elif not re.findall(r'[,，]', query):
            keys = re.findall(r'(\S+)', query)
            # 1 word with no space tail
            if keys.__len__() == 1 and query[-1:] != " ":
                mode, keywords, tags = "Nodes", [query.strip()], []
            # 1 word with space tail & >= 2 words
            else:
                mode, keywords, tags = "Keywords", keys, []
        # 1 comma
        elif re.findall(r'[,，]', query).__len__() == 1:
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
        elif re.findall(r'[,，]', query).__len__() > 2:
            cls.show("2(≥) commas are not allowed!")
            mode, keywords, tags = "", [], []
        else:
            cls.show(["Error!", "Can't parse the input: \'{0}\'".format(query)])
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
