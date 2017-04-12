#-*- coding: utf-8 -*-

import io
import pymysql


class MysqlOutputAdapter(object):
    _conn = None
    _table_name = ''
    _column_count = 0
    _insert_query = None

    def __init__(self, conninfo, table_name):
        self._conn = pymysql.connect(
                        host=conninfo['host'],
                        user=conninfo['user'],
                        password=conninfo['password'],
                        db=conninfo['db'],
                        charset=conninfo['charset'],
                        cursorclass=pymysql.cursors.DictCursor)

        self._table_name = table_name
        self._insert_query = self._create_query()

    def _get_columns_count_from_table(self):
        query = "select count(1) as count from information_schema.columns" \
                " where table_name = '{}';".format(self._table_name)

        with self._conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            out = int(row['count'])

        return out

    def _create_query(self):
        buffer = io.StringIO()
        self._column_count = self._get_columns_count_from_table()

        if self._column_count  < 1:
            raise Exception("The table doesn't have any column. Column count: " + str(self._column_count))

        buffer.write("INSERT INTO ")
        buffer.write(self._table_name)
        buffer.write("( tid, amount, price, timestamp )") # todo:
        buffer.write(" VALUES (")
        for i in range(self._column_count - 1):
            buffer.write("%s,");
        buffer.write("%s);")
        query = buffer.getvalue()
        buffer.close()

        return query

    def write(self, row):

        with self._conn.cursor() as cursor:
            cursor.execute(self._insert_query, row)

        self._conn.commit()

    def close(self):
        self._conn.close()


class MysqlInputAdapter(object):
    _conn = None
    _table_name = ''
    _column_count = 0
    _select_query = None
    _cursor = None

    def __init__(self, conninfo, table_name):
        self._conn = pymysql.connect(
                        host=conninfo['host'],
                        user=conninfo['user'],
                        password=conninfo['password'],
                        db=conninfo['db'],
                        charset=conninfo['charset'],
                        cursorclass=pymysql.cursors.DictCursor)

        self._table_name = table_name


    def _get_columns_count_from_table(self):
        query = "select count(1) as count from information_schema.columns" \
                " where table_name = '{}';".format(self._table_name)

        with self._conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            out = int(row['count'])

        return out

    def run(self, select_query) :
        self._select_query = select_query
        with self._conn.cursor() as cursor:
            cursor.execute(self._select_query)
            self._cursor = cursor

    def readone(self):
        return self._cursor.fetchone()

    def close(self):
        self._conn.close()
