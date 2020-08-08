#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 28th 2020
# ------------------------------------------------


from Items import Display
from New import New
from Utils import Utils as U
import Config as C
import os

query = U.get_query()
option, arg = query.split('|')

if option == "open":
    # U.output(arg)
    U.open(arg)
elif option == "new":
    genre, title = arg.strip('[]').split(", ")
    path = New.new(title, genre)
    # U.output(path)
    U.open(path)
elif option == "delete":
    path, file_name = arg.strip('[]').split(", ")
    U.delete(path)
    U.notify(f"{file_name} has been successfully deleted!")
elif option == "link":
    link = arg
    U.to_clipboard(link)
elif option == "back":
    input_str = arg
    os.system(
        """osascript -e \
        'tell application id "com.runningwithcrayons.Alfred" \
        to run trigger "search" in workflow "com.konfido.pkmanager" \
        with argument "{}"'
        """.format(input_str))
elif option == "refresh":
    os.system('bash ./update_meta.sh')

# config's submenu
elif option == "reset_config":
    key = arg
    value = C.Config().reset(key)
    U.notify("Done!", f"{key} is reset to default: {value}.")

elif option == "reset_all_configs":
    C.Config.reset_all()
    U.notify("Done!", "All configs have been reset to defaults.")

elif option in ["open_config_file", "open_template"]:
    U.open(arg)
    target = option.split("_")[1]
    U.notify(f"Edit the {target} with care! Do not break it!")

elif option == "swap_config":
    key = arg
    value = C.Config().swap(key)
    U.notify("Done!", f"{key} is changed to {value}.")

elif option == "set_config":
    key, value = arg.strip('[]').split(", ")
    if value:
        C.Config().set(key, value)
        U.notify("Done!", f"{key} is set to {value}.")
    else:
        U.notify("Not a valid value. Please retry.")

else:
    U.notify(f"Error! {option}: {arg}", log=True)
