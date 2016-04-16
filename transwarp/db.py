#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'wcx'

'''
Database operation module.
'''
# class Db(object):
# def __init__(self):
#     print "Db init"
#     super(Db, self).__init__()
#     conn = MySQLdb.connect("127.0.0.1", "wcx", "3624249", "dffa")
#     cursor = conn.cursor()
#     cursor.execute("create database if not exists dffa")
#     cursor.execute(
#         "create table if not exists testcase(id int,package varchar(30),activity varchar(30),"
#         "file_name varchar(30),file_type varchar(30),app_name varchar(30),"
#         "version_code varchar(30),version_name varchar(30))")
#     conn.close()
#
#
#  def
import MySQLdb


class MySQLHelper:
    HOST = '127.0.0.1'
    USER = 'wcx'
    PASSWORD = '3624249'
    DBNAME = 'dffa'
    CHARSET = 'utf8'
    TABLE = "testcase"

    def __init__(self, host=HOST, user=USER, password=PASSWORD, db=DBNAME, table=TABLE, charset=CHARSET):
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
            self.cur.execute("create database if not exists %s" % self.db)
            self.conn.select_db(self.db)
            self.cur.execute(
                "create table if not exists %s(id int not null primary key auto_increment,"
                "package varchar(30),activity varchar(30),"
                "file_name varchar(30),file_type varchar(30),app_name varchar(30),"
                "version_code varchar(30),version_name varchar(30))" % self.table)

        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


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


def queryAll(self, sql):
    self.query(sql)
    result = self.cur.fetchall()
    desc = self.cur.description
    d = []
    for inv in result:
        _d = {}
    for i in range(0, len(inv)):
        _d[desc[i][0]] = str(inv[i])
    d.append(_d)
    return d


def insert(self, p_table_name, p_data):
    for key in p_data:
        p_data[key] = "'" + str(p_data[key]) + "'"
    key = ','.join(p_data.keys())
    value = ','.join(p_data.values())
    real_sql = "INSERT INTO" + p_table_name + "(" + key + ") VALUES (" + value + ")"
    # self.query("set names 'utf8'")
    return self.query(real_sql)


def getLastInsertId(self):
    return self.cur.lastrowid


def rowcount(self):
    return self.cur.rowcount


def commit(self):
    self.conn.commit()


def close(self):
    self.cur.close()
    self.conn.close()


if __name__ == '__main__':
    sqlhelper = MySQLHelper()
    print "go go"
