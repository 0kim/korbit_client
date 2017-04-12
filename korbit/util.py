#-*- coding: utf-8 -*-

import json
from datetime import datetime


def load_properties(json_filename):
    with open(json_filename, 'r') as f:
        properties = json.load(f)

    return properties

def now_str():
    return str(datetime.now())

class timer(object):
    _start = 0

    def __init__(self):
        pass

    def start(self):
        self._start = datetime.now()

    def stop(self):
        end = datetime.now()

        return end - self._start
