#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 16th 2020
# ------------------------------------------------


"""
Alfred Script Filter generator class
"""

import json
import os
import sys
import time
from plistlib import readPlist, writePlist


class Items(object):
    """ To generate Script Filter object """

    def __init__(self):
        self.items = []

    def setKv(self, key, value):
        self.item.update({key: value})

    def addItem(self, item):
        """ An item example:
        {   "title": str
            "subtitle": str
            "arg":
            "type":
            "icon": { "type": ""|"image"
                      "path": "icons/hashtag.png" }}
        """
        self.items.append(item)

    def getItems(self, response_type="json"):
        """ get the final items of the script filter output """
        if response_type not in {"json", "dict"}:
            raise ValueError("Type must be in: %s" % {"json", "dict"})

        out = {"items": self.items}

        if response_type == "dict":
            return out
        elif response_type == "json":
            return json.dumps(out)

    def write(self, response_type='json'):
        """ Generate Script Filter Output """
        output = self.getItems(response_type=response_type)
        sys.stdout.write(output)

    @staticmethod
    def debug(cls, message):
        cls.addItem({
            "title": "Debug message",
            "subtitle": "{0}".format(message)
        })
        cls.write()


class Utils(object):

    @staticmethod
    def getEnv(var):
        """ Reads environment variable """
        return os.getenv(var) if os.getenv(var) is not None else str()

    @staticmethod
    def getArgv(i):
        """ Get i-th argument values from input """
        try:
            return sys.argv[i]
        except IndexError:
            return str()
