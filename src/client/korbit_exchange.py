import requests
import json

CATEGORY = {
    'all' : 'all',  # 매수/매도 모두
    'bid' : 'bid',  # 매도
    'ask' : 'ask'   # 매수
}

TIME = {
    'hour': 'hour',
    'minute': 'minute',
    'day': 'day'
}

CURRENCY_PAIR = 'btc_krw'


class KorbitExchage(object):

    def __init__(self):
        return

    def getLatestBid(self):
        bids = self.getOrderbook(category=CATEGORY['bid'])
        return bids['bids'][0]

    def getLatestAsk(self):
        asks = self.getOrderbook(category=CATEGORY['ask'])
        return asks['asks'][0]


    # 매도/매수 호가
    def getOrderbook(self, category='all'):
        try:
            CATEGORY[category]
        except KeyError:
            raise Exception('Unrecognized category: ' + category)

        params = {
            "current_pair": CURRENCY_PAIR
        }

        # curl -D - "https://api.korbit.co.kr/v1/orderbook?currency_pair=$CURRENCY_PAIR"
        url = "https://api.korbit.co.kr/v1/orderbook"
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        output = json.loads(r.text)

        if category == CATEGORY['ask']:
            output.pop('bids')  # bids
        elif category == CATEGORY['bid']:
            output.pop('asks')  # bids
        else:
            pass # =all

        return output


    # 체결 내역
    def getFilledOrders(self, time='hour'): # time = {hour, minute, day}
        try:
            TIME[time]
        except KeyError:
            raise Exception('Unrecognized time: ' + TIME[time])

        params = {
            "current_pair": CURRENCY_PAIR,
            "time": time
        }

        # curl -D - "https://api.korbit.co.kr/v1/transactions?currency_pair=$CURRENCY_PAIR"
        url = "https://api.korbit.co.kr/v1/transactions"
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise Exception("Status code: " + str(r.status_code) + " , body: " + r.text)

        output = json.loads(r.text)

        return output




