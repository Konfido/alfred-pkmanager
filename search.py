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


if not U.getEnv("MARKDOWN_PATH"):
    U.show(("Error!", "Please first set the environment variables of \"MARKDOWN_PATH\"."))

# Load Env variables
query = U.getArgv(1)




mode, keywords, tags = U.parsedArg()


U.show(mode, keywords, tags)


exit(0)


l = Items()
