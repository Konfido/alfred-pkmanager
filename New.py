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
import threading


class New():

    @classmethod
    def show_templates(cls):
        """Show available templates.
        The input content `query` are accepted as the name of new file.

        But once ',' appears in it, `Snippet` will be selected as target templates,
        and `query` will be seperated to be language's name and title accrodingly.
        """
        query = U.get_query()
        arg = query if query else U.get_now()
        (language, title) = arg.split(', ') if ',' in arg else ("<blank>", arg)
        items = []
        for template_path in U.get_all_files_path(C.TEMPLATE_DIR):
            genre = U.get_file_name(template_path)
            if genre == "Snippet":
                items.append({
                    "title": "Create a new Snippet: Input \"<languag>, <title>\"",
                    "subtitle": f"Language: {language}, Name: {title}",
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
        _id = U.get_now("%Y%m%d%H%M%S")
        file_name = title if genre == "Topic" else _id
        new_file_path = U.path_join(file_dir, file_name+'.md')

        content_replace_map = {
            '{title}': title,
            '{tag}': "[]",
            '{datetime}': U.get_now(C.Config().configs["date_format"]),
            '{language}': language,
            '{id}': _id,
        }

        template_path = U.path_join(C.TEMPLATE_DIR, genre+".md")

        with open(template_path, 'r') as f:
            content = U.str_replace(f.read(), content_replace_map)
        if not U.path_exists(new_file_path):
            with open(new_file_path, "w") as f:
                f.write(content)

        return new_file_path


if __name__ == "__main__":
    C.Config().templates_checked()
    New().show_templates()
