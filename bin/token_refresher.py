#-*- coding: utf-8 -*-

from datetime import datetime
from korbit.auth.auth_context import AuthContext
import requests
import json

def getNowStr():
    return datetime.now().strftime('%Y-%m-%d %T %z')

KORBIT_REFRESH_URL = "https://api.korbit.co.kr/v1/oauth2/access_token"
KORBIT_REFRESH_DATA_FORMAT \
    = '{{ "grant_type":"refresh_token", "client_id":"{}", "client_secret":"{}", "refresh_token":"{}"}}'

ctx = AuthContext()

fmt_data = KORBIT_REFRESH_DATA_FORMAT.format(ctx.getClientId(),
                                             ctx.getClientSecret(),
                                             ctx.getRefreshToken())

# print(json.loads(fmt_data))
r = requests.post(KORBIT_REFRESH_URL, data=json.loads(fmt_data))

if r.status_code == 200:
    # Success
    out = json.loads(r.text)
    print("loading... output of json...")
    ctx.updateTokens(out['access_token'], out['refresh_token'], getNowStr())
    print('ACCESS_TOKEN=' + ctx.getAccessToken())
    print('REFRESH_TOKEN=' + ctx.getRefreshToken())
    ctx.saveAuthContext()
    print("[Done]")

else:
    # Fail
    print(r.headers)
    print(r)
    print(r.text)
    print("[Failed]")
