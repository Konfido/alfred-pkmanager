#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  August 1st 2020
# ------------------------------------------------


from Utils import Utils as U
from Items import Items, Display
# from Config import Config
import Config
import threading


C = Config.Config().configs


class New():

    @classmethod
    def new(cls, title, genre='Note', language=''):
        """ create a new file accroding to template """

        # illigal characters for the file name
        title_replace_map = {
            ',': '-',
            '，': '-',
            '.': '_',
            '/': '-',
            ':': '-',
            '#': '-'
        }

        # get new file's title and path
        file_dir = C[f'path_to_new_{genre}']
        file_dir = U.path_join(file_dir, U.get_now("%Y/%m/")) \
            if genre == 'Journal' else file_dir
        U.mkdir(file_dir)      # Create month's subfolder for Journal

        title = U.str_replace(title.strip(), title_replace_map)
        _id = U.get_now("%Y%m%d%H%M%S")
        file_name = {
            "Journal": U.get_now("%Y-%m-%d"),
            "Topic": title
        }
        file_name = file_name[genre] if genre in file_name else _id
        new_file_path = U.path_join(file_dir, file_name+'.md')
        if U.path_exists(new_file_path):
            return new_file_path

        # get date
        date = U.get_now("%Y-%m-%d")
        time = U.get_now("%H:%M:%S")
        date_time = U.get_now("%Y-%m-%d %H:%M:%S")
        date_journal = U.get_now("%B %d, %A")

        # get location
        loc_dict = U.get_corelocation()
        if loc_dict['subLocality']:
            location = f'{loc_dict["address"]},{loc_dict["subLocality"]}'
        else:
            location = loc_dict["address"]

        # get weather
        lat = loc_dict["latitude"]
        lon = loc_dict["longitude"]
        api = C["weather_api"]
        weather = U.get_weather(lat, lon, api, C["locale"]) if api else ""

        content_replace_map = {
            '{title}': title,
            '{tags}': "[]",
            '{date_time}': date_time,
            '{date_journal}': date_journal,
            '{date}': date,
            '{time}': time,
            '{language}': language,
            '{id}': _id,
            '{location}': location,
            '{weather}': weather,
        }

        template_path = U.path_join(Config.TEMPLATE_DIR, genre+".md")

        with open(template_path, 'r') as f:
            content = U.str_replace(f.read(), content_replace_map)
        if not U.path_exists(new_file_path):
            with open(new_file_path, "w") as f:
                f.write(content)

        return new_file_path


def show_templates():
    """ Show available templates.

    If your input content (env $query) does not contain semicolon (',' or '，'), it will be taken as the name of new file.

    Otherwise, it will be seperated into two part and be taken as language's name and note's title of the new Snippet.
    """
    query = U.get_query()
    arg = query if query else U.get_now()
    (language, title) = arg.split(',') if ',' in arg else ("<blank>", arg)
    items = []
    for genre in C["templates"]:
        if genre == "Snippet":
            items.append({
                "title": 'Create a new Snippet: Use "," to seperate "language" and "title"',
                "subtitle": f"Language: {language}, Name: {title.strip()}",
                "arg": f"new|[Snippet>{arg}]"
            })
        elif ',' not in arg:
            subtitle = query if query else U.get_now()+" (Default)"
            items.append({
                "title": f"Create a new {genre}",
                "subtitle": f'Name: {subtitle}',
                "arg": f"new|[{genre}>{arg}]"
            })

    Display.show(items)


if __name__ == "__main__":
    Config.Config().templates_checked()
    show_templates()
