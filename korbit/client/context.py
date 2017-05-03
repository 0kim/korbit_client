#-*- coding: utf-8 -*-

# The following properties must be specified in the 'context.json' file
#
# ACCESS_TOKEN
# REFRESH_TOKEN
# LAST_REFRESH_TIME
# NONCE

import json
import logging

logger = logging.getLogger(__file__)

NONCE_INCREMENT = 2

class Context(object) :
    _context = None
    _ctx_file = None

    def __init__(self, file):
        self._ctx_file = file
        self._loadContext()
        pass

    def _loadContext(self):
        with open(self._ctx_file, 'r') as f:
            self._context = json.load(f)
            f.close()

    def reloadContext(self):
        self._loadContext()

    def saveContext(self):
        with open(self._ctx_file, 'w') as f:
            json.dump(self._context, f, sort_keys=True, indent=4)
            f.close()
        logger.info("Context is saved to " + self._ctx_file)

    def getContext(self):
        return self._context

    def printContext(self):
        print(self._context)

    def updateTokens(self, access_token, refresh_token, last_refresh_time):
        self._context['ACCESS_TOKEN'] = access_token
        self._context['REFRESH_TOKEN'] = refresh_token
        self._context['LAST_REFRESH_TIME'] = last_refresh_time
        self.saveContext()

    def getRefreshToken(self):
        return self._context['REFRESH_TOKEN']

    def getAccessToken(self):
        return self._context['ACCESS_TOKEN']

    def getNonce(self):
        return self._context['NONCE']

    # todo: separate it from
    def increaseNonce(self):
        self._context['NONCE'] += NONCE_INCREMENT
        self.saveContext()
        return self._context['NONCE']




