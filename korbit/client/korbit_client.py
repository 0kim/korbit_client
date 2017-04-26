#-*- coding: utf-8 -*-

import json
import requests
from korbit.auth.auth_context import AuthContext
import korbit.auth.token as token
import logging

logger = logging.getLogger(__file__)

TYPE = {
        'limit': 'limit', # 지정가 주문
        'market': 'market' # 시장가 주문
}
CURRENCY_PAIR = 'btc_krw'

class KorbitClient(object):
    _ctx = None

    def __init__(self):
        self._ctx = AuthContext()
        return

    def _getHeadersWithAccessToken(self):
        hearders = {"Authorization": "Bearer " + self._ctx.getAccessToken()}
        return hearders

    def _getNonce(self):
        return self._ctx.increaseNonce()

    def getUserInfo(self):
        # curl - D - -H "Authorization: Bearer $ACCESS_TOKEN" https: // api.korbit.co.kr / v1 / user / info
        url = "https://api.korbit.co.kr/v1/user/info"

        r = requests.get(url, headers=self._getHeadersWithAccessToken())
        if r.status_code == 401:
            token.token_refresh()
            self._ctx.reloadAuthContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return r.text


    def getTransaction(self):
        return


    def buy(self, price, coin_amount):
        # curl -D - -X POST -H "Authorization: Bearer $ACCESS_TOKEN"
        # -d "currency_pair=$CURRENCY_PAIR&type=$TYPE&price=$PRICE&coin_amount=$COIN_AMOUNT&nonce=$NONCE"
        # https://api.korbit.co.kr/v1/user/orders/buy

        url = "https://api.korbit.co.kr/v1/user/orders/buy"
        data = {
            "current_pair": CURRENCY_PAIR,
            "type": TYPE['limit'],
            "price": price,
            "coin_amount": coin_amount,
            "nonce": self._getNonce()
        }

        # print(data)

        r = requests.post(url, headers=self._getHeadersWithAccessToken(), data=data)
        if r.status_code == 401:
            token.token_refresh()
            self._ctx.reloadAuthContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return json.loads(r.text)   # {"orderId":4140410,"status":"success" ,"currencyPair":"btc_krw"}


    def sell(self, price, coin_amount):
        # curl -D - -X POST -H "Authorization: Bearer $ACCESS_TOKEN"
        # -d "currency_pair=$CURRENCY_PAIR&type=$TYPE&price=$PRICE&coin_amount=$COIN_AMOUNT&nonce=$NONCE"
        # https://api.korbit.co.kr/v1/user/orders/sell

        url = "https://api.korbit.co.kr/v1/user/orders/sell"
        data = {
            "current_pair": CURRENCY_PAIR,
            "type": TYPE['limit'],
            "price": price,
            "coin_amount": coin_amount,
            "nonce": self._getNonce()
        }

        # print(data)

        r = requests.post(url, headers=self._getHeadersWithAccessToken(), data=data)
        if r.status_code == 401:
            token.token_refresh()
            self._ctx.reloadAuthContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return json.loads(r.text)   # {"orderId":4140437,"status":"success","currencyPair":"btc_krw"}


    def getOpenOrders(self, offset=0, limit=10):
        # curl -D - -H "Authorization: Bearer $ACCESS_TOKEN"
        # https://api.korbit.co.kr/v1/user/orders/open?currency_pair=$CURRENCY_PAIR

        url = "https://api.korbit.co.kr/v1/user/orders/open"
        params = {
            "current_pair": CURRENCY_PAIR,
            "offset": offset,
            "limit": limit
        }

        # print(data)

        r = requests.get(url, headers=self._getHeadersWithAccessToken(), params=params)
        if r.status_code == 401:
            token.token_refresh()
            self._ctx.reloadAuthContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return json.loads(r.text)


    def getWallet(self):
        # curl - D - -H
        # "Authorization: Bearer $ACCESS_TOKEN"
        # https://api.korbit.co.kr/v1/user/wallet?currency_pair=$CURRENCY_PAIR

        url = "https://api.korbit.co.kr/v1/user/wallet"
        params = {
            "current_pair": CURRENCY_PAIR,
        }

        r = requests.get(url, headers=self._getHeadersWithAccessToken(), params=params)
        if r.status_code == 401:
            token.token_refresh()
            self._ctx.reloadAuthContext()
            r = requests.get(url, headers=self._getHeadersWithAccessToken())

        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        return json.loads(r.text)

