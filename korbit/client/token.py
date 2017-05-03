#-*- coding: utf-8 -*-

import json
import logging

import requests

from korbit import util as util
from korbit.client.context import Context

KORBIT_REFRESH_URL = "/v1/oauth2/access_token"
KORBIT_REFRESH_DATA_FORMAT \
    = '{{ "grant_type":"refresh_token", "client_id":"{}", "client_secret":"{}", "refresh_token":"{}"}}'

logger = logging.getLogger(__file__)

def token_refresh():
    ctx = Context()

    fmt_data = KORBIT_REFRESH_DATA_FORMAT.format(ctx.getClientId(),
                                                 ctx.getClientSecret(),
                                                 ctx.getRefreshToken())
    logger.info("Loaded token:" + fmt_data)
    logger.info("Request to refresh access token.")
    r = requests.post(KORBIT_REFRESH_URL, data=json.loads(fmt_data))
    if r.status_code == 200:
        # Success
        out = json.loads(r.text)
        logger.info("Loading refresh token...")
        ctx.updateTokens(out['access_token'], out['refresh_token'], util.now_str())
        logger.warning('New access token=' + ctx.getAccessToken())
        logger.warning('New refresh token=' + ctx.getRefreshToken())
        ctx.saveContext()
        logger.info("Successfully updated an access token")
    else:
        # Fail
        logger.warning("Unable to refresh an access token: ")
        logger.warning(r.headers)
        logger.warning(r)
        logger.info(r.text)
        raise Exception("")