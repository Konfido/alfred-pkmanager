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

# Load Env variables
query = U.getArgv(1)

l = Items()

l.addItem({
    "title": "Debug",
    "subtitle":"{0}".format(query)
})
l.write()



exit(0)
