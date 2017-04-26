#-*- coding: utf-8 -*-

from datetime import datetime

import pymysql

import korbit.client.adapter as kbadapter
from korbit.client.korbit_exchange import KorbitExchage
from util import util

TABLE_NAME = 'all_transactions'
prop_mysql = util.load_properties('../adapter_mysql.json')

kbexchnage = KorbitExchage()
mywriter = kbadapter.MysqlOutputAdapter(prop_mysql, TABLE_NAME)

transactions = kbexchnage.getFilledOrders(time='day')

count_pk_duplication = 0
count_insertion_success = 0

timer = util.timer()
timer.start()

for t in transactions:
    row = (t['tid'],          #1
           t['amount'],       #2
           t['price'],        #3
           datetime.fromtimestamp(t['timestamp'] / 1000)) #4
    # print(row)
    try:
        mywriter.write(row)
        count_insertion_success += 1
    except pymysql.err.IntegrityError:
        count_pk_duplication += 1
        pass

elapsed_time = timer.stop()

mywriter.close()

print(util.now_str() +
      " Result: " +
      " elapsed time: " + str(elapsed_time) +
      ", success records: " + str(count_insertion_success) +
      ", ignored records: " + str(count_pk_duplication))
