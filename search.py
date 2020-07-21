#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 16th 2020
# ------------------------------------------------


import sys
import json
from PKM import Items
from PKM import Utils as U
from PKM import Search as S
from PKM import Note
# from Customization import SETTINGS


if not U.get_env_varibles():
    exit(0)

# Load env variables
wiki_path, notes_path = U.get_env_varibles()
# Parse search input
mode, keywords, tags = U.get_parsed_arg()


I = Items()
# S = Search()

sorted_file_list = S.get_sorted_files(notes_path)

if mode == "Recent":

    for f in sorted_file_list:
        c_date = U.format_date(f['ctime'], "%Y-%m-%d")
        m_date = U.format_date(f['mtime'], "%Y-%m-%d")
        I.addItem({
            "title": f['title'],
            "subtitle": u"Modified: {0}, Created: {1}, ({2} Actions, {3} Quicklook)".format(
                m_date, c_date, u'\u2318', u'\u21E7'),
            "type": 'file',
            "arg": f['path']
        })

    if len(I.getItems(response_type="dict")['items']) == 0:
        I.addItem({
            "title": "Nothing found...",
            "subtitle": "Do you want to create a new note with title \"{0}\"?".format(
                query),
            "arg": query
        })
    I.write()
    exit(0)
elif mode == "WIKI":
    pass
elif mode == "Keywords":
    pass
elif mode == "Both":
    pass
elif mode == "Tags":
    pass

I.write()

exit(0)
