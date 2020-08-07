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

notes_path = U.get_abspath(U.get_env("notes_path")).split(",")
wiki_path = U.get_abspath(U.get_env("wiki_path")).split(",")

DEFAULTS = {
    # path to your Markdown App
    # 'app_path': '/Applications/Typora.app',
    # path to your Wiki
    # 'wiki_path': '~/Documents/Sync/Docs_Wiki/010 - Wiki/',
    # path to your notes, multi-path & sub-path is allowed
    # 'notes_path': ['~/Documents/Sync/Docs_Wiki/'],
    # search tags in yaml only or in full content: True/False
    'search_yaml_tag_only': True,
    # present which todo in the top: newest/oldest
    'todo_order': 'newest',
    # quantity of results: Int
    'result_nums': 20,
    # default date format used by templates's YAML info
    'date_format': '%Y-%m-%d %H:%M:%S',
    # set default [template, path] for deferent genre of newly created files.
    'path_to_new_note': notes_path[0],
    'path_to_new_wiki': wiki_path[0],
    'path_to_new_todo': notes_path[0],
    'path_to_new_journal': notes_path[0],

    'templates': {},
    'destination': {}.update()
}


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
