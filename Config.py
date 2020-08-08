#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 20th 2020
# ------------------------------------------------


import os

from Items import Items, Display
from Utils import Utils as U
import json


config_dir = U.get_env("alfred_workflow_data")
config_path = U.path_join(config_dir, "config.json")
template_dir = U.path_join(config_dir, "templates")
templates = [U.get_file_name(f) for f in U.get_all_files_path(template_dir)]

# list of abs_path to your notes, multi-path & sub-path is allowed
notes_path = U.get_abspath(U.get_env("notes_path")).split(",")
# list of abs_path to your Wiki
wiki_path = U.get_abspath(U.get_env("wiki_path")).split(",")
# default path to the file created by templates
default_path = notes_path[0]

DEFAULTS = {
    # path to your Markdown App
    # 'app_path': '/Applications/Typora.app',
    # search tags in yaml only or in full content: True/False
    'search_yaml_tag_only': True,
    # present which todo in the top: newest/oldest
    'todo_order': 'newest',
    # quantity of results: Int
    'result_nums': 20,
    # default date format used by templates's YAML info
    'date_format': '%Y-%m-%d %H:%M:%S',
    # template list: ['wiki', 'note', 'todo', 'journal', 'snippet', ...]
    'templates': templates
}

DEFAULTS.update(dict([(f'path_to_new_{t}', default_path) for t in templates]))


class Config():

    def __init__(self):
        self.configs = self._load_all()

    @staticmethod
    def _load_all():
        """ Get user's local config """
        return U.json_load(config_path)

    def get(self, key):
        return self.configs[key]

    def update(self, key, value):
        """ check and update value """
        if key == "result_nums":
            value = U.literal_eval(value)
            value = value if isinstance(value, int) else 20
        self.configs.update({key: value})
        U.json_dump(self.configs, config_path)

    def swap(self, key):
        if key == "search_yaml_tag_only":
            value = not self.get(key)
        elif key == "todo_order":
            value = "nearest" if self.get(key) == "oldest" else "oldest"
        self.update(key, value)
        return value

    def set(self, key, value):
        self.update(key, value)

    def reset(self, key):
        self.configs.update({key: DEFAULTS[key]})
        U.json_dump(self.configs, config_path)
        return DEFAULTS[key]

    @staticmethod
    def reset_all():
        """ create or reset all """
        U.json_dump(DEFAULTS, config_path)

    @classmethod
    def templates_checked(cls):
        # Move templates to local folder
        if not U.path_exists(template_dir):
            U.mkdir(template_dir)
        for source in U.get_all_files_path(U.get_cwd()+"/templates"):
            name = U.get_file_name(source, with_ext=True)
            target = U.path_join(template_dir, name)
            if not U.path_exists(target):
                U.copy(source, target)
        # Check if any new template put in the user's folder
        templates_now = templates.copy()
        for t in cls().configs["templates"]:
            templates_now.remove(t)
        if templates_now:
            for t in templates_now:
                cls().set(f'path_to_new_{t}', default_path)
            cls().set("templates", templates)