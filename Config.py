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
TEMPLATES_PATH_DEFAULT = [f for f in U.get_all_files_path(U.get_cwd()+"/templates")]
TEMPLATES_NAME_DEFAULT = [U.get_file_name(f) for f in TEMPLATES_PATH_DEFAULT]

# root dir to all your files, which is a must to resolve relative paths in Markdown Links or Back Links.
# ROOT_PATH = [U.get_abspath(p) for p in U.get_env("root_path").split(",")]
# abs_path to your notes, only one path is allowed
NOTES_PATH = [U.get_abspath(p) for p in U.get_env("notes_path").split(",")]
# list of abs_path to your files, multi-path & sub-path is allowed
FILES_PATH = [U.get_abspath(p) for p in U.get_env("files_path").split(",")]
# default path to the file created by templates: notes_path
DEFAULT_PATH = NOTES_PATH[0]


DEFAULTS = {
    # path to your Markdown App
    # 'app_path': '/Applications/Typora.app',
    # search tags in yaml only or in full content: True/False
    'search_tag_yaml_only': True,
    # search snippets by languages specified in yaml only or including code fences: True/False
    'search_snippet_yaml_only': True,
    # snippet searching result will be combined and returned same when language appears in a alias tuple.
    'language_alias': [('sh','bash','shell'), ('python','py')],
    # present which todo in the top: newest/oldest
    'todo_order': 'newest',
    # quantity of results: Int
    'result_nums': 20,
    # search scope: only search [Todo/Snippet/Notes] in its own folders or in all files_path: True/False
    'search_all_folders': False,
    # template list: ['wiki', 'note', 'todo', 'journal', 'snippet', ...]
    'templates': TEMPLATES_NAME_DEFAULT,
    # open weather api
    'weather_api': "",
    # language of auto-completed text in templates
    'locale': U.get_locale()[0],
}

DEFAULTS.update(
    dict([(f'path_to_new_{t}', DEFAULT_PATH) for t in TEMPLATES_NAME_DEFAULT]))

# Workflow Filter's format
WF_SHOW_SUBTITLE = "{folder} | {mdate} | <\u2318-Actions, \u21E7-Quicklook>"
# WF_NEW_CONFIG = "new|{genre}>{title}"

class Config():
    """ Use `Config().configs` to fetch curent config dict"""
    # TODO: refraction is needed
    def __init__(self):
        self.configs = self._load_all()

    @staticmethod
    def _load_all():
        """ Get user's local config """
        return U.json_load(CONFIG_PATH)

    def get(self, key):
        return self.configs[key]

    def remove(self, key):
        self.configs.pop(key)
        U.json_dump(self.configs, CONFIG_PATH)

    def update(self, key, value):
        """ check and update value """
        if key == "result_nums":
            value = U.literal_eval(value)
            value = value if isinstance(value, int) else 20
        self.configs.update({key: value})
        U.json_dump(self.configs, CONFIG_PATH)

    def swap(self, key):
        if key in ["search_tag_yaml_only", "search_snippet_yaml_only", "search_all_folders"]:
            value = not self.get(key)
        elif key == "todo_order":
            value = "nearest" if self.get(key) == "oldest" else "oldest"
        self.update(key, value)
        return value

    def set(self, key, value):
        "alias to update()"
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
        templates_path_now = [f for f in U.get_all_files_path(TEMPLATE_DIR)]
        templates_name_now = [U.get_file_name(n) for n in templates_path_now]
        templates_record = Config().configs['templates']
        record_copy = templates_record.copy() # to keep templates' sequence

        # test_list = templates_name_now.copy()
        if not U.path_exists(TEMPLATE_DIR):
            U.mkdir(TEMPLATE_DIR)
        # Create default templates if it's inexistent/deleted
        for source in TEMPLATES_PATH_DEFAULT:
            name = U.get_file_name(source)
            target = U.path_join(TEMPLATE_DIR, name+".md")
            if not U.path_exists(target):
                # User-defined templates created
                U.copy(source, target)
                templates_name_now.append(name)
        # Add path to new user-defined templates
        for i in templates_name_now:
            if i in templates_record:
                templates_record.remove(i)
            else:
                cls().set(f'path_to_new_{i}', DEFAULT_PATH)
                record_copy.append(i)
        # Delete path to deleted user-defined templates
        for j in templates_record:
            cls().remove(f'path_to_new_{j}')
            record_copy.remove(j)
        # Update config of 'templates'
        cls().set("templates", record_copy)
        return
