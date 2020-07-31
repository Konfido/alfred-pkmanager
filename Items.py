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

    def add_item(self, arg):
        """ Allowed arg structure: int/float/str/dict/list/tuple """
        if isinstance(arg, list) or isinstance(arg, tuple):
            for i in arg:
                self.add_item(i)
        elif isinstance(arg, dict):
            self.items.append(arg)
        else:
            try:
                self.items.append({"title": arg})
            except Exception as e:
                self.items.append({"title": "Exception!", "subtitle": e})

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


class Display():
    """  Customize SrciptFilter to show specific content """

    @staticmethod
    def show(*args):
        """ Send common messages to script filter """
        I = Items()
        for arg in args:
            I.add_item(arg)
        I.write()

    @classmethod
    def none_matched(cls, mode, query):
        genre = "Wiki" if mode == "Wiki" else "Note"
        cls.show({
            "title": "Nothing found...",
            "subtitle": "Presh '\u2318' and 'Enter' to create a new \"{0}\" with title \"{1}\"".format(
                genre, query),
            "arg": "{}|{}".format("None", query),
            "mods": {
                "cmd": {
                    "arg": "{}|{}".format("New", [mode, query]),
                    "subtitle": "Press 'Enter' to complete"}}})

    @classmethod
    def matched_result(cls, dicted_files, query):
        items = []
        for f in dicted_files:
            items.append({
                "title": f['title'],
                "subtitle": u"Modified: {0}, ({1} Actions, {2} Quicklook)".format(
                    f['mdate'], u'\u2318', u'\u21E7'),
                "type": 'file',
                "arg": "{}|{}".format("Open", f['path']),
                "mods": {
                    "cmd": {
                        "arg": "{}|{}".format("Next", [f['path'], query]),
                        "subtitle": "Press 'Enter' to select your next action"}}})
        cls.show(items)

    @classmethod
    def config_options(cls):
        """  Config options """
        Display.show(
            {   "title": "Set configurations",
                "subtitle": "Press 'Enter' to select",
                "arg": "{}|{}".format("select_config", "")
            },
            {   "title": "Open the config file",
                "subtitle": "This will open a json config file with your default application.",
                "arg": "{}|{}".format("open_config", "")
            },
            {   "title": "Reset all configurations",
                "subtitle": "Configs will be reverted to default. This can't be undone!",
                "arg": "{}|{}".format("reset_config", "")
            })
