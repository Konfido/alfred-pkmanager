#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 27th 2020
# ------------------------------------------------

import json
import sys

from Utils import Utils as U


class Items():
    """ To generate Script Filter item """

    def __init__(self):
        self.items = []
        self.item = {
            # "title": "xxx",           # str, title
            # "subtitle": "xxx",        # str, subtitle
            # "arg": "xxx",             # str, arg parsed to next
            # "type": "xxx",            # str, file
            # "autocomplete": "xxx",    # str, auto completed after enter
            # "icon": {
            #     "type": "xxx",        # str, "fileicon" | "image"
            #     "path": "xxx"         # str, path to file/image
            # },
            # "mods": {
            #     "xxx": {              # str, "alt" | "cmd" | "shift" | "ctrl" | "fn"
            #         "valid": "xxx",   # boolean, validity of the mod
            #         "arg": "xxx",     # str, return to next
            #         "subtitle": "xxx" # str, subtitle showed under mod
            #     }
            # }
        }

    def add_item(self, item):
        """ add an item / item_list """
        if isinstance(item, list):
            for i in item:
                self.items.append(i)
        else:
            self.items.append(item)

    def add_mod_all(self, mod, arg, subtitle, valid=True, icon_type="", icon_path=""):
        """ Add one mod to self.items """
        para = {"arg": arg, "subtitle": subtitle, "valid": valid}
        icon = {"icon_type": icon_type, "icon_path": icon_path}
        for item in self.items:
            item["mods"].update({mod: para})
            item.update({"icon": icon})

    def write(self):
        """ Generate Script Filter Output """
        out = json.dumps({"items": self.items})
        sys.stdout.write(out)


    ##  Customize SrciptFilter to show specific content

    @classmethod
    def show_none_matched(cls, mode, query):
        cls.__init__(cls)
        genre = "Wiki" if mode == "Wiki" else "Note"
        cls.add_item(cls, {
            "title": "Nothing found...",
            "subtitle": "Presh '\u2318' and 'Enter' to create a new \"{0}\" with title \"{1}\"".format(
                genre, query),
            "arg": "{}|{}".format("None", query),
            "mods": {
                "cmd": {
                    "arg": "{}|{}".format("New", [mode, query]),
                    "subtitle": "Press 'Enter' to complete"}}})
        cls.write(cls)

    @classmethod
    def show_matched_result(cls, dicted_files, query):
        cls.__init__(cls)
        for f in dicted_files:
            cls.add_item(cls, {
                "title": f['title'],
                "subtitle": u"Modified: {0}, ({1} Actions, {2} Quicklook)".format(
                    f['mdate'], u'\u2318', u'\u21E7'),
                "type": 'file',
                "arg": "{}|{}".format("Open", f['path']),
                "mods": {
                    "cmd":{
                        "arg": "{}|{}".format("Next", [f['path'], query]),
                        "subtitle": "Press 'Enter' to select your next action"}}})
        cls.write(cls)

    @classmethod
    def show(cls, *args):
        """ Used under debugging: Send debug message to script filter

        Allowed input format:
            - String/Int/Float/List -> Title
            - Tuple: T[0] -> Title; T[1] -> Subtitle
            - Dict: {"Title": "xx", "Subtitle": "xx"}
        """
        cls.__init__(cls)

        for item in args:

            try:
                if isinstance(item, str) or isinstance(item, int) or isinstance(item, float):
                    cls.add_item(cls, {"title": item})
                    continue
                if isinstance(item, list):
                    for i in item:
                        cls.add_item(cls, {"title": i})
                    continue
                elif isinstance(item, tuple):
                    title = item[0]
                    subtitle = item[1]
                elif isinstance(item, dict) and item.has_key("title"):
                    title = item["title"]
                    subtitle = item["subtitle"] if item.has_key(
                        "subtitle") else ""
                else:
                    cls.add_item(cls, {"title": "Error!",
                                "subtitle": "Filter {}".format(item)})
                    continue

                cls.add_item(cls, {"title": title,
                            "subtitle": subtitle})
            except Exception as e:
                cls.add_item(cls, {"title": "Exception!",
                            "subtitle": e})

        cls.write(cls)
