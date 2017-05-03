import json
from korbit.client.korbit_exchange import KorbitExchage

properties_sandbox = "../properties_sandbox_test.json"

kbexchnage = KorbitExchage(properties_sandbox)

print( kbexchnage.getOrderbook(category='all') )
out = kbexchnage.getFilledOrders(time='day')
print(json.dumps(out))
print(kbexchnage.getLatestBid())
print(kbexchnage.getLatestAsk())