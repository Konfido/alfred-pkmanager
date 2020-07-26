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
from Customization import Configuration as C


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


class Utils():

    @staticmethod
    def get_env(var):
        """ Reads environment variable """
        return os.getenv(var) if os.getenv(var) is not None else str()

    @staticmethod
    def get_abspath(path):
        return os.path.expanduser(os.getenv(path))

    @classmethod
    def get_env_varibles(cls):
        """ Check valibility of env variables"""
        for env in ["MARKDOWN_APP","NOTES_PATH","WIKI_PATH"]:
            if not cls.get_env(env):
                cls.show((  "ERROR: Find empty environt varibles!",
                            "Please check: \"{}\".".format(env) ))
                return False
        for path in cls.get_env("NOTES_PATH").split(","):
            if not(os.path.exists(path)):
                cls.show((  "ERROR: Find invalid directory!",
                            "Please check \"NOTES_PATH\": {}".format(path)))
                return False
        if not cls.get_env("WIKI_PATH"):
            cls.show((  "ERROR: Find invalid directory!",
                        "Please check \"WIKI_PATH\""))
            return False

        notes_path = cls.get_abspath("NOTES_PATH").split(",")
        wiki_path = cls.get_abspath("WIKI_PATH").split(",")
        return (wiki_path, notes_path)

    @staticmethod
    def get_query():
        return  sys.argv[1].lower()

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
                    subtitle = item["subtitle"] if item.has_key("subtitle") else ""
                else:
                    cls.add_item({ "title": "Error!",
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


class Note():
    def __init__(self, path):
        # super().__init__()
        self.path = os.path.abspath(path)

    def _get_file_name(self):
        file_name = os.path.basename(self.path)[:-len('.md')]
        return file_name

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

    def _get_file_title(self, content):
        file_name = self._get_file_name(self)
        yaml_title = self.get_yaml_item("title", content)
        level_one_title = re.search(r'^# (\s+)', content)
        title = yaml_title or level_one_title or file_name or ""
        return title

    @classmethod
    def get_file_info(cls, path):
        """ get file's info in dict """

        cls.path = path
        name = cls._get_file_name(cls)
        content = cls.get_file_content(path).lower()
        title = cls._get_file_title(cls, content).lower()
        file_stats = os.stat(cls.path)
        ctime_float = file_stats.st_birthtime
        mtime_float = file_stats.st_mtime
        cdate_string = Utils.format_date(ctime_float, "%Y-%m-%d")
        mdate_string = Utils.format_date(mtime_float, "%Y-%m-%d")
        size = file_stats.st_size
        file_infos = {
            'path': path,
            'file_name': name,
            'content': content,
            'title': title,
            'cdate': cdate_string,
            'mdate': mdate_string,
            'ctime': ctime_float,
            'mtime': mtime_float,
            'size': size
        }
        return file_infos

    @staticmethod
    def check_filename(s):
        Utils.str_replace(s, SETTINGS.title_replace_map)
        pass

    @staticmethod
    def new(title, genre=''):
        """ create a new file accroding to template """

        if genre not in ['wiki', 'note', 'todo']:
            Utils.notify("Unsupported template: {}".format(template))
            return None

        template = SETTINGS['type'][genre][0]
        template_file = os.path.join(
            SETTINGS['template_path'], template.join(".md"))

        file_path = SETTINGS['type'][genre][1]
        file = os.path.join(file_path, title.join('.md'))
        replace_map = {
            '{title}': title.strip(),
            '{tag}': "[]",
            '{datetime}': Utils.get_now()
        }

        with open(template_file, r) as f:
            content = Utils.str_replace(f.read(), replace_map)

        if not os.path.exists(file):
            with open(file, w) as f:
                f.write(content)

        return file
