#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 26th 2020
# ------------------------------------------------

import datetime
import os
import re
import sys
import time
import json
import ast
import shutil

class Utils():

    @staticmethod
    def get_env(var):
        """ Reads environment variable """
        return os.getenv(var) if os.getenv(var) is not None else str()

    @staticmethod
    def get_abspath(path):
        return os.path.expanduser(path)

    @staticmethod
    def get_cwd():
        return os.getcwd()

    @staticmethod
    def path_exists(path):
        return os.path.exists(path)

    @staticmethod
    def mkdir(path):
        return os.makedirs(path)

    @staticmethod
    def path_join(root, file):
        return os.path.join(root, file)

    @staticmethod
    def json_load(file):
        with open(file, 'r') as f:
            var = json.load(f)
        return var

    @staticmethod
    def json_dump(var, file):
        with open(file, 'w') as f:
            json.dump(var, f, indent=4)

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
                    mode, keywords, tags = "Wiki", [query.strip()], []
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
                mode, keywords, tags = "GT2", [], []
            else:
                cls.log(
                    ("Error!", "Can't parse the input: \'{0}\'".format(query)))
                raise

        return mode, keywords, tags

    @classmethod
    def get_all_files_path(cls, paths):
        """ support multi note paths """
        file_paths_list = []
        if isinstance(paths, str):
            paths = [paths]
        for path in paths:
            path = cls.get_abspath(path)
            # support subfolders
            for root, dirs, files in os.walk(path):
                for name in files:
                    if name.endswith(".md"):
                        file_paths_list.append(os.path.join(root, name))
        return file_paths_list

    @staticmethod
    def log(message):
        sys.stderr.write('LOG: {0}\n'.format(message))

    @staticmethod
    def notify(title, text="PKManger"):
        """ Send Notification to mac Notification Center """
        os.system("""osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))

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

    @staticmethod
    def output(string):
        sys.stdout.write(string)

    @staticmethod
    def open_file(path):
        os.system("open \"{}\"".format(path))

    @staticmethod
    def literal_eval(var):
        return ast.literal_eval(var)
        # return eval(var)

    @classmethod
    def copy(cls, source, target):
        """copy source file to target """
        shutil.copy(source, target)
