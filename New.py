#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  August 1st 2020
# ------------------------------------------------


from Utils import Utils as U
from Items import Items, Display
# from Config import Config
import Config as C


class New():

    @classmethod
    def show_templates(cls):
        C.Config().templates_checked()
        items = []
        for template_path in U.get_all_files_path(C.TEMPLATE_DIR):
            genre = U.get_file_name(template_path)
            name = query if query else U.get_now()
            subtitle = query if query else U.get_now()+" (Default)"

            items.append({
                "title": f"Create a new {genre}",
                "subtitle": f'Name: {subtitle}',
                "arg": f"new|[{genre}, {name}]"
            })

        Display.show(items)

    @classmethod
    def new(cls, title, genre='Note', language=''):
        """ create a new file accroding to template """

        # illigal characters for the file name
        title_replace_map = {
            # ' ': '_',
            ',': '-',
            '，': '-',
            '.': '_',
            '/': '-',
            ':': '-',
            '#': '-'
        }

        file_dir = C.Config().configs[f'path_to_new_{genre}']
        title = U.str_replace(title.strip(), title_replace_map)
        new_file_path = U.path_join(file_dir, title+'.md')

        content_replace_map = {
            '{title}': title,
            '{tag}': "[]",
            '{datetime}': U.get_now(C.Config().configs["date_format"]),
            '{language}': language,
        }

        template_path = U.path_join(C.TEMPLATE_DIR, genre+".md")

        with open(template_path, 'r') as f:
            content = U.str_replace(f.read(), content_replace_map)
        if not U.path_exists(new_file_path):
            with open(new_file_path, "w") as f:
                f.write(content)

        return new_file_path


if __name__ == "__main__":
    query = U.get_query()
    New().show_templates()
