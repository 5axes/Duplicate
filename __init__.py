# Copyright (c) 2020 Lalliard
# The Duplicate plugin is released under the terms of the AGPLv3 or higher.

from . import Duplicate

def getMetaData():
    return {}

def register(app):
    return {"extension": Duplicate.Duplicate()}
