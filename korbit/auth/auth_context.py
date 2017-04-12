#-*- coding: utf-8 -*-

import json

AUTH_CONTEXT_FILE = '../authcontext.json'

class AuthContext(object) :
    _auth_context = None

    def __init__(self):
        self._loadAuthContext()
        pass

    def _loadAuthContext(self):
        with open(AUTH_CONTEXT_FILE, 'r') as f:
            self._auth_context = json.load(f)
            f.close()

    def reloadAuthContext(self):
        self._loadAuthContext()

    def saveAuthContext(self):
        with open(AUTH_CONTEXT_FILE, 'w') as f:
            json.dump(self._auth_context, f, sort_keys=True, indent=4)
            f.close()
        print("auth context is saved...")

    def getAuthContext(self):
        self._loadAuthContext()

        return self._auth_context

    def printAuthContext(self):
        self._loadAuthContext()
        print(self._auth_context)

    def updateTokens(self, access_token, refresh_token, last_refresh_time):
        self._auth_context['ACCESS_TOKEN'] = access_token
        self._auth_context['REFRESH_TOKEN'] = refresh_token
        self._auth_context['LAST_REFRESH_TIME'] = last_refresh_time

    def getRefreshToken(self):
        return self._auth_context['REFRESH_TOKEN']

    def getAccessToken(self):
        return self._auth_context['ACCESS_TOKEN']

    def getClientId(self):
        return self._auth_context['CLIENT_ID']

    def getClientSecret(self):
        return self._auth_context['CLIENT_SECRET']






