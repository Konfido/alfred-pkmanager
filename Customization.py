#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 20th 2020
# ------------------------------------------------


import os

from Items import Items
from Utils import Utils as U
import json


CONFIG_PATH = U.get_env("alfred_workflow_data")
CONFIG_FILE = U.path_join(CONFIG_PATH, "config.json")

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
    'new_note_path': '',
    'new_wiki_path': '',
    'new_todo_path': 'newest_first',
    'new_journal_path': '',

    # allowed file extension
    # "ext": ['md']
    # used for iAwriter
    # 'url_scheme': 'x-marked://open/?file=',
}


class Config():

    def __init__(self):
        self._configs = self._load_all()
        self.configs = {
            "result_nums": self._configs['result_nums'],
            "date_format": self._configs['date_format'],
            "search_yaml_tag_only": self._configs['search_yaml_tag_only'],
            "new_note_path": self._configs['new_note_path'],
            "new_wiki_path": self._configs['new_wiki_path'],
            "new_journal_path": self._configs['new_journal_path'],
            "new_todo_path": self._configs['new_todo_path'],
            "todo_order": self._configs['todo_order'],
        }

    @classmethod
    def varibles_checked(cls):
        # Check validity of Workflow env variables
        for env in ["markdown_app", "notes_path", "wiki_path"]:
            if not U.get_env(env):
                Items().show(("ERROR: Find empty environt varibles!",
                              "Please check: \"{}\".".format(env)))
                return False
        for path in U.get_env("notes_path").split(","):
            if not(U.path_exists(U.get_abspath(path))):
                Items().show(("ERROR: Find invalid directory!",
                              "Please check \"notes_path\": {}".format(path)))
                return False
        if not U.get_env("wiki_path"):
            Items().show(("ERROR: Find invalid directory!",
                          "Please check \"wiki_path\""))
            return False

        # Create local configuration file
        if not U.path_exists(CONFIG_PATH):
            U.mkdir(CONFIG_PATH)
        if not U.path_exists(CONFIG_FILE):
            cls.reset_all()
        else:
            try:
                cls._load_all()
            except Exception as e:
                Items.show(e)
                #TODO: reset all config/go check?
                return False

        return True

    @staticmethod
    def _load_all():
        """ Get user's local config """
        with open(CONFIG_FILE, 'r') as f:
            configs = json.load(f)
        return configs

    def get(self, key):
        return self.configs[key]

    def update(self, key, value):
        self.configs.update({key, value})

    def reset(self, key):
        self.configs.update({key, DEFAULTS[key]})
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.configs, f, indent=4)

    @staticmethod
    def reset_all():
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULTS, f, indent=4)
