#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido
# Created Date:  July 26th 2020
# ------------------------------------------------

import ast
import datetime
import json
import locale
import os
import re
import shutil
import sys
import time
import urllib.request


class Utils():

    # ---------------------
    #     Basic Utils
    # ---------------------

    @staticmethod
    def open(path, finder=False):
        """ open file / folder """
        if finder:
            os.system("open -R \"{}\"".format(path))
        else:
            os.system("open \"{}\"".format(path))

    @classmethod
    def delete(cls, path):
        """ Delete the selected file"""
        # Files can only be detected as `Removed` in `fswatch` when
        # you conduct the `rm` command. Hence we copy the file to Trash
        # before the actual removal to avoid incorrect deletion.
        cls.copy(path, "~/.Trash")
        os.remove(path)

    @classmethod
    def copy(cls, source, target):
        """copy source file/folder to target """
        shutil.copy(cls.get_abspath(source), cls.get_abspath(target))

    @staticmethod
    def format_date(float_date, fmt="%Y-%m-%d %H:%M:%S"):
        """ float time to string """
        return time.strftime(fmt, time.localtime(float_date))

    @staticmethod
    def get_now(fmt="%Y-%m-%d %H:%M:%S"):
        """ Get formated current date&time string """
        now = datetime.datetime.now()
        return now.strftime(fmt)

    @classmethod
    def get_locale(cls):
        loc = locale.getlocale()
        return loc

    @classmethod
    def mkdir(cls, path):
        """Check if dir exists and recursively mkdir"""
        if not cls.path_exists(path):
            os.makedirs(path)
            return 1
        else:
            return 0

    @staticmethod
    def get_cwd():
        return os.getcwd()

    @classmethod
    def get_abspath(cls, path, query_dict=False):
        """Return str() if get error """
        if path.startswith('~/'):
            abs_path = os.path.expanduser(path)
        elif path.startswith('/Users'):
            abs_path = path
        elif query_dict == True:
            # convert relative_path to abs_path by querying stored path's info
            file_name = os.path.basename(path)
            paths_dict = cls.json_load(cls.path_join(
                cls.get_env("alfred_workflow_data"), 'paths.json'))
            try:
                abs_path = paths_dict[file_name]
            except KeyError:
                abs_path = ""
        else:
            abs_path = path
        return abs_path

    @classmethod
    def get_relpath(cls, path, start):
        relpath = os.path.relpath(path, start)
        return relpath

    @classmethod
    def path_exists(cls, path):
        return os.path.exists(path)

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
    def str_replace(string, replace_map):
        for r in replace_map.keys():
            string = string.replace(r, replace_map[r])
        return string

    @staticmethod
    def literal_eval(var):
        return ast.literal_eval(var)
        # return eval(var)

    # ------------------------------------------------
    #    Advanced Utils: fetch information
    # ------------------------------------------------

    @staticmethod
    def get_env(var):
        """ Reads environment variable """
        return os.getenv(var) if os.getenv(var) is not None else str()

    @staticmethod
    def get_query(lower=False):
        try:
            query = sys.argv[1].lower() if lower else sys.argv[1]
        except:
            query = ""
        return query

    @staticmethod
    def get_search_type():
        try:
            search_type = sys.argv[2]
        except:
            search_type = 'normal'
        return search_type

    @staticmethod
    def get_file_meta(path, key):
        """Get file's size, ctime, mtime"""
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

    # @staticmethod
    @classmethod
    def get_typora_filename(cls):
        """
        Return
            file's name,    if any note opened in Typora
            "",          if otherwise
        """
        filename = os.popen("""osascript <<EOF
        tell application "System Events"
	        get name of front window of process "Typora"
        end tell\nEOF""")
        return filename.read().strip()

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
    def get_corelocation():
        """Return a dict of corelocation's info"""
        corelocation = os.popen('swift ./corelocation.swift -json').read()
        null = ''
        loc_dict = eval(corelocation)
        loc_dict['address'] = loc_dict['address'].replace('\n', ',')
        return loc_dict

    @classmethod
    def get_weather(cls, lat, lon, api, lang=""):
        lang = cls.get_locale()[0] if not lang else lang
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&lang={lang}"
        response = urllib.request.urlopen(url)
        html = response.read().decode("utf-8")
        weather = json.loads(html)
        return weather["weather"][0]['description']

    # ------------------------------------------------
    #    Advanced Utils: perform operation
    # ------------------------------------------------

    @staticmethod
    def output(string):
        sys.stdout.write(string)

    @staticmethod
    def log(message):
        sys.stderr.write('LOG: {0}\n'.format(message))

    @classmethod
    def notify(cls, message, title="PKManger", log=False):
        """ Send Notification to mac Notification Center """
        # os.system("""osascript -e 'display notification "{}" with title "{}"'
        #           """.format(message, title))
        os.system("""./terminal-notifier.app/Contents/MacOS/terminal-notifier \
            -title "{}" -message "{}" \
            -appIcon icon.png \
            -sender com.runningwithcrayons.Alfred \
            -group com.runningwithcrayons.Alfred""".format(title, message))
        if log:
            cls.log(message)

    @staticmethod
    def to_clipboard(content):
        os.system(
            """osascript -e \
            'tell application "System Events" to set the clipboard to "{}"'
            """.format(content))
