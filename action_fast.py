#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------
# Created by Konfido on 2020-07-28
# --------------------------------------


from Items import Display
from New import New
from Utils import Utils as U
import Config
import os
from Search import Search as S

query = U.get_query()
option, arg = query.split('|')

if option == "open":
    # U.output(arg)
    U.open(arg)
elif option == "new":
    genre, arg = arg.strip('[]').split(">")
    if genre == "Snippet":
        language, title = arg.split(", ")
    else:
        language, title = "", arg
    path = New.new(title, genre, language)
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
    # Update stored dict of note's pathes
    paths_list = U.get_all_files_path(Config.FILES_PATH)
    paths = {}
    for p in paths_list:
        file_name = os.path.basename(p)
        paths[file_name] = p
    U.json_dump(paths, U.path_join(Config.CONFIG_DIR, 'paths.json'))
    # refresh updated time
    os.system('bash ./update_meta.sh')
    # update synonyms
    sorted_wiki_list = S.get_sorted_files(Config.NOTES_PATH)
    synonyms = {}
    for wiki in sorted_wiki_list:
        synonym = U.get_yaml_item("synonyms", wiki['content'])
        if synonym and synonym != '[]':
            synonyms.update({wiki['title']: synonym.strip('[]').split(',')})
    U.json_dump(synonyms, U.path_join(Config.CONFIG_DIR, "synonyms.json"))
    U.notify("Done! Synonyms.json has been updated.")
    # update backlinks
    sorted_note_list = S.get_sorted_files(Config.FILES_PATH)

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
