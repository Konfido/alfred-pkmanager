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

        file_dir = C().configs['path_to_new_file'][genre]
        title = U.str_replace(title, title_replace_map)
        new_file_path = U.path_join(file_dir, title+'.md')

        replace_map = {
            '{title}': title.strip(),
            '{tag}': "[]",
            '{datetime}': U.get_now(C().configs["date_format"]),
            '{language}': language,
        }

        # use default format if not configured
        template_dir = template_dir if C(
        ).configs["template"][genre] != 'Default_{}'.format(genre) else './templates'

        template_path = U.path_join(template_dir, genre+".md")

        with open("./templates/{}.md".format(genre), 'r') as f:
            content = U.str_replace(f.read(), replace_map)
        if not U.path_exists(new_file_path):
            with open(new_file_path, "w") as f:
                f.write(content)

        return new_file_path
