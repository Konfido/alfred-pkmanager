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


def update_synonyms_lookup(path="", all=False):
    """ Update the stored lookup of synonyms """
    def _update(path, synonyms={}):
        info = File.get_file_info(path)
        match = info['synonyms']
        if match and match != '[]':
            synonyms.update({info['title']: match.strip('[]').split(',')})
        elif info['title'] in synonyms:
            synonyms.pop(info['title'])
        return synonyms

    if all == False:
        synonyms = U.json_load(U.path_join(Config.CONFIG_DIR, 'synonyms.json'))
        synonyms = _update(path, synonyms)
    else:
        synonyms = {}
        for path in U.get_all_files_path(Config.NOTES_PATH):
            synonyms = _update(path, synonyms)
    U.json_dump(synonyms, U.path_join(Config.CONFIG_DIR, "synonyms.json"))

def update_paths_lookup(path="", type="Created", all=False):
    """ Update the stored lookups of note's paths """

    if all == False:
        paths = U.json_load(U.path_join(Config.CONFIG_DIR, 'paths.json'))
        if type == "Created":
            paths.update({os.path.basename(path): path})
        elif type == "Removed":
            paths.pop(os.path.basename(path))
    else:
        paths = {}
        for p in U.get_all_files_path(Config.FILES_PATH):
            paths.update({os.path.basename(p): p})
    U.json_dump(paths, U.path_join(Config.CONFIG_DIR, 'paths.json'))

def update_backlinks_lookup(path="", all=False):
    """ Update the stored lookup of backlinks """
    def _update(path, backlinks={}):
        links = S.markdown_links_search(path)
        if links:
            for link in links:
                name = os.path.basename(link)
                backs = set((backlinks[name])) if name in backlinks else set()
                backs.add(path)
                backlinks.update({name: list(backs)})
        return backlinks

    if all == False:
        backlinks = U.json_load(U.path_join(Config.CONFIG_DIR, 'backlinks.json'))
        backlinks = _update(path, backlinks)
    else:
        backlinks = {}
        for path in U.get_all_files_path(Config.NOTES_PATH):
            backlinks = _update(path, backlinks)
    U.json_dump(backlinks, U.path_join(Config.CONFIG_DIR, "backlinks.json"))


if __name__ == "__main__":
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
        # refresh updated time
        os.system('bash ./update_meta.sh')

    # config's submenu
    elif option == "update":
        update_synonyms_lookup(all=True)
        U.notify("synonyms.json updated.")

        update_paths_lookup(all=True)
        U.notify("paths.json updated.")

        update_backlinks_lookup(all=True)
        U.notify("backlinks.json updated.")
        U.notify("Done!")

    elif option == "auto_update":
        os.system(f"bash ./update_lookup.sh {arg} >/dev/null 2>&1 &")

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
