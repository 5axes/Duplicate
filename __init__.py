# Copyright (c) 2020 5@xes
# The Duplicate plugin is released under the terms of the AGPLv3 or higher.

from . import Duplicate

def getMetaData():
    return {}

def register(app):
    return {"extension": Duplicate.Duplicate()}
