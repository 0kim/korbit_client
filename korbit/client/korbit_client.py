#-*- coding: utf-8 -*-

import json
import logging
import time
import requests

from korbit.client.context import Context
from korbit.client.properties import Properties
from korbit.util import util

logger = logging.getLogger(__file__)

TYPE = {
        'limit': 'limit', # 지정가 주문
        'market': 'market' # 시장가 주문
}
CURRENCY_PAIR = 'btc_krw'
WAIT_INTERVAL_SEC = 5

# CONTEXT_FILE_PRODUCTION = 'context.json'
# PROPERTIES_FILE_PRODUCTION = 'properties.json'
# CONTEXT_FILE_SANDBOX = 'context_sandbox.json'
# PROPERTIES_FILE_SANDBOX = 'properties_sandbox.json'

class KorbitClient(object):
    _properties = None
    _ctx = None

    def __init__(self, prop_file, ctx_file):
        self._properties = Properties(prop_file)
        self._ctx = Context(ctx_file)

    def _getHeadersWithAccessToken(self):
        headers = {"Authorization": "Bearer " + self._ctx.getAccessToken()}
        return headers

    def _getNonce(self):
        return self._ctx.increaseNonce()

    def _refreshAccessToken(self):
        TOKEN_REFRESH_URL = "/v1/oauth2/access_token"
        TOKEN_REFRESH_DATA_FMT  \
            = '{{ "grant_type":"refresh_token", "client_id":"{}", "client_secret":"{}", "refresh_token":"{}"}}'

        fmt_data = TOKEN_REFRESH_DATA_FMT.format(self._properties.getClientId(),
                                                 self._properties.getClientSecret(),
                                                 self._ctx.getRefreshToken())
        logger.info("Request to refresh access token.")

        url = self._properties.getApiUrl() + TOKEN_REFRESH_URL
        r = requests.post(url, data=json.loads(fmt_data))
        if r.status_code == 200:
            # Success
            out = json.loads(r.text)
            logger.info("Loading refresh token...")
            self._ctx.updateTokens(out['access_token'], out['refresh_token'], util.now_str())
            logger.warning('New access token=' + self._ctx.getAccessToken())
            logger.warning('New refresh token=' + self._ctx.getRefreshToken())
            self._ctx.saveContext()
            logger.info("Successfully updated an access token")
        else:
            # Fail
            logger.warning("Unable to refresh an access token: " + str(r.headers))
            raise Exception("Unable to refresh an access token")

    def getUserInfo(self):
        # curl - D - -H "Authorization: Bearer $ACCESS_TOKEN" https: // api.korbit.co.kr / v1 / user / info

        url = self._properties.getApiUrl() + "/v1/user/info"
        r = requests.get(url, headers=self._getHeadersWithAccessToken())
        if r.status_code == 401:
            self._refreshAccessToken()
            self._ctx.reloadContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())
        elif r.status_code == 504: # Gateway time-out
            for i in range (1, 10):
                # wait and re-execute it 10 times
                logger.info(__name__ + " 504 (gateway time-out) wait " +
                            str(WAIT_INTERVAL_SEC) + " seconds and re-execute. Try " + str(i))
                time.wait(WAIT_INTERVAL_SEC)
                r = requests.get(url, headers=self._getHeadersWithAccessToken())
                if r.status_code != 504:
                    break;

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return r.text

    def getTransaction(self):
        return


    def buy(self, price, coin_amount):
        # curl -D - -X POST -H "Authorization: Bearer $ACCESS_TOKEN"
        # -d "currency_pair=$CURRENCY_PAIR&type=$TYPE&price=$PRICE&coin_amount=$COIN_AMOUNT&nonce=$NONCE"
        # https://api.korbit.co.kr/v1/user/orders/buy

        url = self._properties.getApiUrl() + "/v1/user/orders/buy"
        data = {
            "current_pair": CURRENCY_PAIR,
            "type": TYPE['limit'],
            "price": price,
            "coin_amount": coin_amount,
            "nonce": self._getNonce()
        }

        logger.debug(data)

        r = requests.post(url, headers=self._getHeadersWithAccessToken(), data=data)
        if r.status_code == 401:
            self._refreshAccessToken()
            self._ctx.reloadContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())
        elif r.status_code == 504:  # Gateway time-out
            for i in range(1, 10):
                # wait and re-execute it 10 times
                logger.info(__name__ + " 504 (gateway time-out) wait " +
                            str(WAIT_INTERVAL_SEC) + " seconds and re-execute. Try " + str(i))
                time.wait(WAIT_INTERVAL_SEC)
                r = requests.post(url, headers=self._getHeadersWithAccessToken(), data=data)
                if r.status_code != 504:
                    break;

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return json.loads(r.text)   # {"orderId":4140410,"status":"success" ,"currencyPair":"btc_krw"}


    def sell(self, price, coin_amount):
        # curl -D - -X POST -H "Authorization: Bearer $ACCESS_TOKEN"
        # -d "currency_pair=$CURRENCY_PAIR&type=$TYPE&price=$PRICE&coin_amount=$COIN_AMOUNT&nonce=$NONCE"
        # https://api.korbit.co.kr/v1/user/orders/sell

        url = self._properties.getApiUrl() + "/v1/user/orders/sell"
        data = {
            "current_pair": CURRENCY_PAIR,
            "type": TYPE['limit'],
            "price": price,
            "coin_amount": coin_amount,
            "nonce": self._getNonce()
        }

        logger.debug(data)

        r = requests.post(url, headers=self._getHeadersWithAccessToken(), data=data)
        if r.status_code == 401:
            self._refreshAccessToken()
            self._ctx.reloadContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())
        elif r.status_code == 504:  # Gateway time-out
            for i in range(1, 10):
                # wait and re-execute it 10 times
                logger.info(__name__ + " 504 (gateway time-out) wait " +
                            str(WAIT_INTERVAL_SEC) + " seconds and re-execute. Try " + str(i))
                time.wait(WAIT_INTERVAL_SEC)
                r = requests.post(url, headers=self._getHeadersWithAccessToken(), data=data)
                if r.status_code != 504:
                    break;

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return json.loads(r.text)   # ex: {"orderId":4140437,"status":"success","currencyPair":"btc_krw"}


    def getOpenOrders(self, offset=0, limit=10):
        # curl -D - -H "Authorization: Bearer $ACCESS_TOKEN"
        # https://api.korbit.co.kr/v1/user/orders/open?currency_pair=$CURRENCY_PAIR

        url = self._properties.getApiUrl() + "/v1/user/orders/open"
        params = {
            "current_pair": CURRENCY_PAIR,
            "offset": offset,
            "limit": limit
        }

        r = requests.get(url, headers=self._getHeadersWithAccessToken(), params=params)
        if r.status_code == 401:
            self._refreshAccessToken()
            self._ctx.reloadContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())
        elif r.status_code == 504:  # Gateway time-out
            for i in range(1, 10):
                # wait and re-execute it 10 times
                logger.info(__name__ + " 504 (gateway time-out) wait " +
                            str(WAIT_INTERVAL_SEC) + " seconds and re-execute. Try " + str(i))
                time.wait(WAIT_INTERVAL_SEC)
                r = requests.get(url, headers=self._getHeadersWithAccessToken(), params=params)
                if r.status_code != 504:
                    break;

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return json.loads(r.text)


    def getWallet(self):
        # curl - D - -H
        # "Authorization: Bearer $ACCESS_TOKEN"
        # https://api.korbit.co.kr/v1/user/wallet?currency_pair=$CURRENCY_PAIR

        url = self._properties.getApiUrl() + "/v1/user/wallet"
        params = {
            "current_pair": CURRENCY_PAIR,
        }

        r = requests.get(url, headers=self._getHeadersWithAccessToken(), params=params)
        if r.status_code == 401:
            self._refreshAccessToken()
            self._ctx.reloadContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())
        elif r.status_code == 504:  # Gateway time-out
            for i in range(1, 10):
                # wait and re-execute it 10 times
                logger.info(__name__ + " 504 (gateway time-out) wait " +
                            str(WAIT_INTERVAL_SEC) + " seconds and re-execute. Try " + str(i))
                time.wait(WAIT_INTERVAL_SEC)
                r = requests.get(url, headers=self._getHeadersWithAccessToken(), params=params)
                if r.status_code != 504:
                    break;

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return json.loads(r.text)

