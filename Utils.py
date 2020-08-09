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
            json.dump(var, f, indent=4, ensure_ascii=False)

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
    def get_query(lower=False):
        try:
            query = sys.argv[1].lower() if lower else sys.argv[1]
        except:
            query = ""
        return query

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

    @classmethod
    def notify(cls, text, title="PKManger", log=False):
        """ Send Notification to mac Notification Center """
        os.system("""osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))
        if log:
            cls.log(text)

    @staticmethod
    def to_clipboard(content):
        os.system(
            """osascript -e \
            'tell application "System Events" to set the clipboard to "{}"'
            """.format(content))

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
    def open(path):
        """ open file / folder """
        os.system("open \"{}\"".format(path))

    @staticmethod
    def delete(path):
        os.remove(path)

    @staticmethod
    def literal_eval(var):
        return ast.literal_eval(var)
        # return eval(var)

    @classmethod
    def copy(cls, source, target):
        """copy source file to target """
        shutil.copy(source, target)
