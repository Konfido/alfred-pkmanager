#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------
# Created by Konfido on 2020-07-28
# --------------------------------------


import os

import Config
import New
from Items import Display
from Search import File
from Search import Search as S
from Utils import Utils as U


query = U.get_query()
option, arg = query.split('|')

if option == "open":
    # U.output(arg)
    U.open(arg)
elif option == "reveal":
    U.open(arg, finder=True)
elif option == "new":
    genre, arg = arg.strip('[]').split(">")
    if genre == "Snippet":
        language, title = arg.split(", ")
    else:
        language, title = "", arg
    path = New.create_new_file(title, genre, language)
    # U.output(path)
    U.open(path)
elif option == "delete":
    path, file_title = arg.strip('[]').split(", ")
    U.delete(path)
    U.notify(f"{file_title} has been successfully deleted!")
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
    # Update the stored lookup for note's pathes
    paths_list = U.get_all_files_path(Config.FILES_PATH)
    paths = {}
    for p in paths_list:
        file_name = os.path.basename(p)
        paths[file_name] = p
    U.json_dump(paths, U.path_join(Config.CONFIG_DIR, 'paths.json'))
    U.notify("paths.json updated.")
    # Update the stored lookup for backlinks
    backlinks = {}
    for path in paths_list:
        links = S.markdown_links_search(path)
        if links:
            for link in links:
                name = os.path.basename(link)
                backlinks[name] = backlinks[name] + \
                    [path] if backlinks.__contains__(name) else [path]
    U.json_dump(backlinks, U.path_join(Config.CONFIG_DIR, "backlinks.json"))
    U.notify("backlinks.json updated.")
    # refresh updated time
    os.system('bash ./update_meta.sh')
    # update synonyms
    sorted_wiki_list = S.get_sorted_files(Config.NOTES_PATH)
    synonyms = {}
    for wiki in sorted_wiki_list:
        synonym = File.get_yaml_item("synonyms", wiki['yaml'])
        if synonym and synonym != '[]':
            synonyms.update({wiki['title']: synonym.strip('[]').split(',')})
    U.json_dump(synonyms, U.path_join(Config.CONFIG_DIR, "synonyms.json"))
    U.notify("synonyms.json updated.")
    U.notify("Done!")

# config's submenu
elif option == "reset_config":
    key = arg
    value = Config.Config().reset(key)
    U.notify("Done!", f"{key} is reset to default: {value}.")

elif option == "reset_all_configs":
    Config.Config.reset_all()
    U.notify("Done!", "All configs have been reset to defaults.")

elif option in ["open_config_file", "open_template"]:
    U.open(arg)
    target = option.split("_")[1]
    U.notify(f"Edit the {target} with care! Do not break it!")

elif option == "swap_config":
    key = arg
    value = Config.Config().swap(key)
    U.notify("Done!", f"{key} is changed to {value}.")

elif option == "set_config":
    key, value = arg.strip('[]').split(", ")
    if value:
        Config.Config().set(key, value)
        U.notify("Done!", f"{key} is set to {value}.")
    else:
        U.notify("Not a valid value. Please retry.")

elif option == "create_weather_api":
    app = "/Applications/Safari.app"
    url = "https://home.openweathermap.org/users/sign_up"
    os.system(f"open -a {app} {url}")

else:
    U.notify(f"Error! {option}: {arg}", log=True)
