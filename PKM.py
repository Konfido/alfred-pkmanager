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
from Customization import Configuration as C
from Utils import Utils as U

class Items():
    """ To generate Script Filter item """

    def __init__(self):
        self.items = []
        self.item = {}

    def add_item(self, item):
        """ An item example:

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
                "alt": {        {str, "alt" | "cmd" | "shift" | "ctrl" | "fn"
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

    def _add_mod(self, mod, arg, subtitle, icon_type, icon_path):
        """Add a mod to item"""

        para = {
            "valid": true,
            "arg": arg,
            "subtitle": subtitle
        }
        self.item["mods"].update({mod, para})
        self.item["icon"].update({"type": icon_type})
        self.item["icon"].update({"path": icon_path})
        return self.item

    def add_mods(self, mods):
        for m in mods:
            self._add_mod(self.item, m)

    def add_none_matched_item(self, query):
        self.add_item({
            "title": "Nothing found...",
            "subtitle": "Do you want to create a new note with title \"{0}\"?".format(
                query),
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

    def get_items(self, response_type="json"):
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
        output = self.get_items(response_type=response_type)
        sys.stdout.write(output)


class Note():
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

    @staticmethod
    def new(title, genre=''):
        """ create a new file accroding to template """

        if genre not in ['wiki', 'note', 'todo']:
            U.notify("Unsupported template: {}".format(template))
            return None

        template = SETTINGS['type'][genre][0]
        template_file = os.path.join(
            SETTINGS['template_path'], template.join(".md"))

        file_path = SETTINGS['type'][genre][1]
        file = os.path.join(file_path, title.join('.md'))
        replace_map = {
            '{title}': title.strip(),
            '{tag}': "[]",
            '{datetime}': U.get_now()
        }

        with open(template_file, r) as f:
            content = U.str_replace(f.read(), replace_map)

        title = U.str_replace(title, SETTINGS.title_replace_map)

        if not os.path.exists(file):
            with open(file, w) as f:
                f.write(content)

        return file
