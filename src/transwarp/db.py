#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings

import MySQLdb

from src.models import TestTarget

warnings.filterwarnings("ignore")

__author__ = 'wcx'

'''
Database operation module.
'''


class MySQLHelper:
    HOST = '127.0.0.1'
    USER = 'wcx'
    PASSWORD = '3624249'
    DBNAME = 'dffa'
    CHARSET = 'utf8'
    TABLE_TARGET = "target"

    def __init__(self, host=HOST, user=USER, password=PASSWORD, db=DBNAME, table=TABLE_TARGET, charset=CHARSET):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.table = table
        self.charset = charset

        try:
            self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password)
            self.conn.set_character_set(self.charset)
            self.cur = self.conn.cursor()
            self.conn.select_db(self.db)
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def init(self):
        self.create_db()
        self.create_table()

    def create_db(self):
        self.cur.execute("create database if not exists %s default character set %s collate utf8_general_ci" % (
            self.db, self.charset))

    def create_table(self):
        self.cur.execute("drop table if exists %s" % self.table)
        sql = "create table {0}" \
              "(id int not null primary key auto_increment," \
              "package varchar(30)," \
              "activity varchar(80)," \
              "action varchar(80)," \
              "category varchar(80)," \
              "mime_type varchar(60)," \
              "file_name varchar(80)," \
              "app_name varchar(30)," \
              "version_code varchar(30)," \
              "version_name varchar(30)," \
              "seed varchar(80))" \
            .format(self.table)

        self.cur.execute(sql)

    def query(self, sql):
        try:
            n = self.cur.execute(sql)
            return n
        except MySQLdb.Error as e:
            print("Mysql Error:%snSQL:%s" % (e, sql))

    def queryRow(self, sql):
        self.query(sql)
        result = self.cur.fetchone()
        return result
        #
        #
        # def queryAll(self, sql):
        #     self.query(sql)
        #     result = self.cur.fetchall()
        #     desc = self.cur.description
        #     d = []
        #     for inv in result:
        #         _d = {}
        #     for i in range(0, len(inv)):
        #         _d[desc[i][0]] = str(inv[i])
        #     d.append(_d)
        #     return d
        #
        #

    def insert(self, p_table_name, p_data):
        for key in p_data:
            p_data[key] = "'" + str(p_data[key]) + "'"
        key = ','.join(p_data.keys())
        value = ','.join(p_data.values())
        real_sql = "INSERT INTO " + p_table_name + "(" + key + ") VALUES (" + value + ")"
        try:
            n = self.cur.execute(real_sql)
            self.commit()
            return n
        except MySQLdb.Error as e:
            print("Mysql Error:%snSQL:%s" % (e, real_sql))

    #
    #
    # def getLastInsertId(self):
    #     return self.cur.lastrowid
    #
    #
    # def rowcount(self):
    #     return self.cur.rowcount
    #
    #
    def commit(self):
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn.open:
            self.conn.close()

    def insert_targets(self, targets):
        for target in targets:
            self.insert(self.TABLE_TARGET, vars(target))

    def query_target(self):
        sql = "select * from {0} where id=68".format(self.TABLE_TARGET)
        result = self.queryRow(sql)
        print result
        target = TestTarget(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8],
                            result[9], result[10])
        return target


if __name__ == '__main__':
    sqlhelper = MySQLHelper()
    # p_data = {'package': "com.test", 'activity': "com.test.act", 'file_name': "/sd/a/a.jpg", 'app_name': "piuk",
    #           'version_code': "123", "version_name": "1.01", "seeds": "~/"}
    # n = sqlhelper.insert(sqlhelper.TABLE_TARGET, p_data)
    print sqlhelper.query_target()
    sqlhelper.close()
