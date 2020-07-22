#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 20th 2020
# ------------------------------------------------


class Configuration():

    SETTINGS = {
        # 'wiki_path': '',
        # 'notes_path': [],
        # search tags in yaml only or in full content: True/False
        'tags_in_yaml_only': True,
        # present which todo in the top: newest/oldest
        'todo_order': 'newest',
        # quantity of results: Int
        'result_nums': 20,
        # default date format used in templates
        'date_format': '%Y-%m-%d %H:%M:%S',
        # default template path
        'template_path': './templates',
        # set default [template, path] for deferent genre of newly created files.
        'type': {
            'note': ['default_note', ""],
            'wiki': ['default_wiki', ""],
            'todo': ['default_todo', ""]
            # 'daily': 'new_note'
        },
        # illigal characters for the file name
        # "illigal_char_list": ['/', '\\', ':', '|', ',', '#'],
        # allowed file extension
        # "ext": ['md']
        # used for iAwriter
        # 'url_scheme': 'x-marked://open/?file=',
    }
