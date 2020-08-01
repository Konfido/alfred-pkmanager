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
    'new_note_path': notes_path[0],
    'new_wiki_path': wiki_path[0],
    'new_todo_path': notes_path[0],
    'new_journal_path': notes_path[0],

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
                Display.show(("ERROR: Find empty environt varibles!",
                              "Please check: \"{}\".".format(env)))
                return False
        for path in U.get_env("notes_path").split(","):
            if not(U.path_exists(U.get_abspath(path))):
                Display.show(("ERROR: Find invalid directory!",
                              "Please check \"notes_path\": {}".format(path)))
                return False
        if not U.get_env("wiki_path"):
            Display.show(("ERROR: Find invalid directory!",
                          "Please check \"wiki_path\""))
            return False

        # Create local configuration file
        if not U.path_exists(config_dir):
            U.mkdir(config_dir)
        if not U.path_exists(config_path):
            cls.reset_all(new=True)
        else:
            try:
                cls._load_all()
            except Exception as e:
                Display.show(e)
                #TODO: reset all config/go check?
                return False

        return True

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
        U.notify("Done!", "{} is changed to {}.".format(key, value))

    def set(self, key, value):
        self.update(key, value)
        U.notify("Done!", "{} is set to {}.".format(key, value))

    def reset(self, key):
        self.configs.update({key: DEFAULTS[key]})
        U.json_dump(self.configs, config_path)
        U.notify("Done!", "{} is reset to {}.".format(key, DEFAULTS[key]))

    @staticmethod
    def reset_all(new=False):
        """ create or reset all """
        U.json_dump(DEFAULTS, config_path)
        if new:
            U.notify("Done!", "All configs are reset to defaults.")


if __name__ == "__main__":
    Display.show(
        {
            "title": "Set configurations",
            "subtitle": "Go next and see the details",
            "arg": "{}|{}".format("select_config", "")
        },
        {
            "title": "Open config file",
            "subtitle": "Open & Modify a JSON formatted config file",
            "arg": "{}|{}".format("open_config", config_path)
        },
        {
            "title": "Open templates folder",
            "subtitle": "Put your Markdown templates files in the folder",
            "arg": "{}|{}".format("open_template", template_dir)
        },
        {
            "title": "Reset all configurations",
            "subtitle": "Configs will be reverted to default. This can't be undone!",
            "arg": "{}|{}".format("reset_config", "")
        },
        )
