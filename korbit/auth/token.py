#-*- coding: utf-8 -*-

import json
import logging

import requests

import util.util as util
from korbit.auth.auth_context import AuthContext

KORBIT_REFRESH_URL = "https://api.korbit.co.kr/v1/oauth2/access_token"
KORBIT_REFRESH_DATA_FORMAT \
    = '{{ "grant_type":"refresh_token", "client_id":"{}", "client_secret":"{}", "refresh_token":"{}"}}'

logger = logging.getLogger(__file__)

def token_refresh():
    ctx = AuthContext()

    fmt_data = KORBIT_REFRESH_DATA_FORMAT.format(ctx.getClientId(),
                                                 ctx.getClientSecret(),
                                                 ctx.getRefreshToken())
    logger.debug("Loaded token:" + json.loads(fmt_data))

    logger.info("Request to refresh access token.")
    r = requests.post(KORBIT_REFRESH_URL, data=json.loads(fmt_data))
    if r.status_code == 200:
        # Success
        out = json.loads(r.text)
        logger.info("Loading refresh token...")
        ctx.updateTokens(out['access_token'], out['refresh_token'], util.now_str())
        logger.debug('New access token=' + ctx.getAccessToken())
        logger.debug('New refresh token=' + ctx.getRefreshToken())
        ctx.saveAuthContext()
        logger.info("Successfully updated an access token")
    else:
        # Fail
        logger.info("Unable to refresh an access token: ")
        logger.debug(r.headers)
        logger.debug(r)
        logger.info(r.text)
        raise Exception("")