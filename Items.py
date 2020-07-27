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
        self.item = {}

    def add_item(self, item):
        """
        {   "title":            str, title
            "subtitle":         str, subtitle
            "arg":              str, arg parsed to next
            "type":             str, file
            "autocomplete":     str, auto completed after enter
            "icon": {
                "type":         str, "fileicon"|"image"
                "path":         str, path to file/image
            }
            "mods": {
                "alt": {        str, "alt" | "cmd" | "shift" | "ctrl" | "fn"
                    "valid":    boolean, validity of the mod
                    "arg":      str, return to next
                    "subtitle"  str, subtitle showed under mod
                },
            }
        }
        """
        # if not item.get("arg"):
        #     item["arg"] = Utils.get_query()
        self.items.append(item)

    def add_mod(self, mod, arg, subtitle, valid=True, icon_type="", icon_path=""):
        """Add one mod to self.items
        mod: ("alt" | "cmd" | "shift" | "ctrl" | "fn")
        """
        para = {"arg": arg, "subtitle": subtitle, "valid": valid}
        icon = {"icon_type": icon_type, "icon_path": icon_path}
        for item in self.items:
            item["mods"].update({mod: para})
            item.update({"icon": icon})

    def add_none_matched_item(self, genre, query):
        title = query if not query else "default"
        self.add_item({
            "title": "Nothing found...",
            "subtitle": "Do you want to create a new {0} with title \"{1}\"?".format(
                genre, title),
            "arg": query,
        })

    def add_result_items(self, dicted_files):
        for f in dicted_files:
            self.add_item({
                "title": f['title'],
                "subtitle": u"Modified: {0}, Created: {1}, ({2} Actions, {3} Quicklook)".format(
                    f['mdate'], f['cdate'], u'\u2318', u'\u21E7'),
                "type": 'file',
                "arg": f['path'],
                # "icon": {
                #     "type": "fileicon",
                #     "path": f['path']
                # },
                "mods": {
                    "command": {
                        "arg": "",
                        "subtitle": "Next Action for this Note"
                    }
                }
            })

    def get_items(self):
        """ get the final items of the script filter output """
        out = {"items": self.items}
        return json.dumps(out)

    def write(self):
        """ Generate Script Filter Output """
        output = self.get_items()
        sys.stdout.write(output)

    # def write(self):
    #     out = {"items": self.items}
    #     out = json.dumps(out)
    #     sys.stdout.write(out)

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

        output = cls.get_items(cls)
        sys.stdout.write(output)
