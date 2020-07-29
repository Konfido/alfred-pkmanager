#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 28th 2020
# ------------------------------------------------


import ast

from Items import Items
from Search import File, Search
from Utils import Utils as U


option, query = U.get_query().split('>')

if option == "open":
    U.output(query)
elif option == "new":
    genre, title = ast.literal_eval(query)
    path = File.new(title, genre)
    U.output(path)
