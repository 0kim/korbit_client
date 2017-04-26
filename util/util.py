#-*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def load_properties(json_filename):
    logger.info("Opening properties file " + json_filename)
    with open(json_filename, 'r') as f:
        properties = json.load(f)

    return properties

def now_str():
    return datetime.now().strftime('%Y-%m-%d %T %z')


class timer(object):
    _start = 0

    def __init__(self):
        pass

    def start(self):
        self._start = datetime.now()

    def stop(self):
        end = datetime.now()

        return end - self._start
