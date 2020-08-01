#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 28th 2020
# ------------------------------------------------


from Items import Display
from New import New
from Utils import Utils as U
from Config import Config


inputs = U.get_query()
option, arg = inputs.split('|')

if option == "open":
    # U.output(arg)
    U.open_file(arg)
elif option == "new":
    genre, title = U.literal_eval(arg)
    path = New.new(title, genre)
    # U.output(path)
    U.open_file(path)

# config's submenu
elif option == "reset_config":
    Config.reset_all()
elif option == "open_config":
    Config.open_file()
elif option == "swap_config":
    Config().swap(arg)
elif option == "set_config":
    key, value = U.literal_eval(arg)
    if value:
        Config().set(key, value)

else:
    Display.show("Error")
