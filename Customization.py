#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 20th 2020
# ------------------------------------------------


# class Configuration():

SETTINGS = {
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
    'new_file_path': {
        'note': '',
        'wiki': '',
        'todo': '',
        'journay': ''
    },
    # illigal characters for the file name
    "title_replace_map" : {
        ' ': '_',
        ',': '-',
        '，': '-',
        '.': '_',
        '/': '-',
        ':': '-',
        '#': '-'
    }
    # allowed file extension
    # "ext": ['md']
    # used for iAwriter
    # 'url_scheme': 'x-marked://open/?file=',
}
