#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  August 1st 2020
# ------------------------------------------------


from Utils import Utils as U
from Items import Items, Display
from Config import Config as C


config_dir = U.get_env("alfred_workflow_data")
config_path = U.path_join(config_dir, "config.json")
template_dir = U.path_join(config_dir, "templates")
# templates = U.get_all_files_path()

# query = U.get_query()


class New():

    @staticmethod
    def templates_checked():
        # Move templates to local folder
        if not U.path_exists(template_dir):
            U.mkdir(template_dir)
        for source in U.get_all_files_path(U.get_cwd()+"/templates"):
            name = 'Default_' + U.get_file_name(source, True)
            target = U.path_join(template_dir, name)
            if not U.path_exists(target):
                U.copy(source, target)

    @classmethod
    def new(cls, title, genre='wiki', language=''):
        """ create a new file accroding to template """

        cls.templates_checked()
        # illigal characters for the file name
        title_replace_map = {
            ' ': '_',
            ',': '-',
            '，': '-',
            '.': '_',
            '/': '-',
            ':': '-',
            '#': '-'
        }

        template = U.path_join('./templates', genre.join(".md"))
        file_root = C().configs['new_{}_path'.format(genre)]
        title = U.str_replace(title, title_replace_map)
        file_path = U.path_join(file_root, '{}.md'.format(title))
        replace_map = {
            '{title}': title.strip(),
            '{tag}': "[]",
            '{datetime}': U.get_now(C().configs["date_format"]),
            '{language}': language,
        }

        with open("./templates/Wiki.md", 'r') as f:
            content = U.str_replace(f.read(), replace_map)

        if not U.path_exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)

        return file_path


if __name__ == "__main__":
    Display.show(
        {"title": "file_name",
         "subtitle": "",
         "arg": "{}|{}".format("", "")
         },
    )
