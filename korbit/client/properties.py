#-*- coding: utf-8 -*-

import json
import logging

logger = logging.getLogger(__file__)

KORBIT_URL_SANDBOX = {
    "API_URL": "https://api.korbit-test.com",
    "SITE_URL": "https://www.korbit-test.com"
}

KORBIT_URL_PRODUCTION = {
    "API_URL": "https://api.korbit.co.kr",
    "SITE_URL": "https://www.korbit.co.kr"
}

class Properties():
    _prop_file = None
    _properties = None
    _is_sandbox = False
    _korbit_url = None

    def __init__(self, file):
        self._prop_file = file
        self._loadProperties()
        pass

    def _loadProperties(self):
        with open(self._prop_file, 'r') as f:
            self._properties = json.load(f)
            f.close()
            if self._properties['IS_SANDBOX'] == True:
                self._korbit_url = KORBIT_URL_SANDBOX
                self._is_sandbox = True
            else:
                self._korbit_url = KORBIT_URL_PRODUCTION
                self._is_sandbox = False

    def isSandbox(self):
        return self._is_sandbox

    def getClientId(self):
        return self._properties['CLIENT_ID']

    def getClientSecret(self):
        return self._properties['CLIENT_SECRET']

    def getApiUrl(self):
        return self._korbit_url['API_URL']

    def getSiteUrl(self):
        return self._korbit_url['SITE_URL']
