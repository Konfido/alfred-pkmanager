#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 20th 2020
# ------------------------------------------------


from Items import Items, Display
from Utils import Utils as U
import json



CONFIG_DIR = U.get_env("alfred_workflow_data")
CONFIG_PATH = U.path_join(CONFIG_DIR, "config.json")
TEMPLATE_DIR = U.path_join(CONFIG_DIR, "templates")
# templates exist in the folder
TEMPLATES = [U.get_file_name(f) for f in U.get_all_files_path(TEMPLATE_DIR)]

# list of abs_path to your notes, multi-path & sub-path is allowed
NOTES_PATH = U.get_abspath(U.get_env("notes_path")).split(",")
# list of abs_path to your Wiki
WIKI_PATH = U.get_abspath(U.get_env("wiki_path")).split(",")
# default path to the file created by templates: wiki_path[0]
DEFAULT_PATH = WIKI_PATH[0]


DEFAULTS = {
    # path to your Markdown App
    # 'app_path': '/Applications/Typora.app',
    # search tags in yaml only or in full content: True/False
    'search_yaml_tag_only': True,
    # present which todo in the top: newest/oldest
    'todo_order': 'newest',
    # quantity of results: Int
    'result_nums': 20,
    # template list: ['wiki', 'note', 'todo', 'journal', 'snippet', ...]
    'templates': TEMPLATES
}

DEFAULTS.update(
    dict([(f'path_to_new_{t}', DEFAULT_PATH) for t in TEMPLATES]))


class Config():

    def __init__(self):
        self.configs = self._load_all()

    @staticmethod
    def _load_all():
        """ Get user's local config """
        return U.json_load(CONFIG_PATH)

    def get(self, key):
        return self.configs[key]

    def update(self, key, value):
        """ check and update value """
        if key == "result_nums":
            value = U.literal_eval(value)
            value = value if isinstance(value, int) else 20
        self.configs.update({key: value})
        U.json_dump(self.configs, CONFIG_PATH)

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
        U.json_dump(self.configs, CONFIG_PATH)
        return DEFAULTS[key]

    @staticmethod
    def reset_all():
        """ create or reset all """
        U.json_dump(DEFAULTS, CONFIG_PATH)

    @classmethod
    def templates_checked(cls):
        # Move templates to local folder
        if not U.path_exists(TEMPLATE_DIR):
            U.mkdir(TEMPLATE_DIR)
        for source in U.get_all_files_path(U.get_cwd()+"/templates"):
            name = U.get_file_name(source, with_ext=True)
            target = U.path_join(TEMPLATE_DIR, name)
            if not U.path_exists(target):
                U.copy(source, target)
        # Check if any new template put in the user's folder
        templates_now = TEMPLATES.copy()
        for t in cls().configs["templates"]:
            templates_now.remove(t)
        if templates_now:
            for t in templates_now:
                cls().set(f'path_to_new_{t}', DEFAULT_PATH)
            cls().set("templates", TEMPLATES)
