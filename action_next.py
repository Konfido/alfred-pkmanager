#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 27th 2020
# ------------------------------------------------


# from Customization import Config as C
from Items import Items
from Utils import Utils as U
import ast

option = U.get_env('next_1')

if option == "Edit":
    path, query = ast.literal_eval(U.get_env('next_2'))
    file_name = U.get_file_name(path)
    m_path, m_type = "icon", "image"

    I = Items()
    I.add_item([
        {
            "title": "Back",
            "subtitle": f"Back to Search with query: {query}",
            # "arg": f"back|{query}",
            "arg": f"back|{query}",
            # "icon": "icons/back.png",
        },
        {
            "title": "Markdown Link",
            "subtitle": f"Copy MD Link for \"{file_name}\" to the Clipboard",
            "arg": f"link|[{file_name}]({path})",
            # "icon": "icons/link.png",
        },
        {
            "title": "Delete Note",
            "subtitle": u"Delete \"{0}\". This action cannot be undone!".format(file_name),
            "arg": f"delete|{path}>{query}",
            # "icon": "icons/delete.png",
        },
    ])
    I.write()
