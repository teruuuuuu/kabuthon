# -*- coding: utf-8 -*-
import os
import sqlite3


def sql_execute(sql):
    return DbConnection().conn.execute(sql)


def sql_executemany(sql, generator):
    return DbConnection().conn.executemany(sql, generator)


def count_sql(sql):
    return DbConnection().conn.execute(sql).fetchall()[0][0]


class DbConnection:
    _instance = None
    db_file = None
    conn = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DbConnection, cls).__new__(cls, *args, **kwargs)
            cls._instance.db_file = os.environ.get("DB_FILE")
        return cls._instance

    def __init__(self):
        self.conn = sqlite3.connect(os.environ.get("DB_FILE"))

    # TODO 一つのself.connを使いまわす場合、複数トランザクション開始するときに__exit__で落ちたりする
    def exclusive(self):
        if self.db_file is None:
            raise ValueError("db file path not set")
        self.conn = sqlite3.connect(self.db_file, isolation_level="EXCLUSIVE")
        return self

    def auto_commit(self):
        if self.db_file is None:
            raise ValueError("db file path not set")
        self.conn = sqlite3.connect(self.db_file)
        return self

    def __enter__(self, *args, **kwargs):
        self.conn.__enter__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        self.conn.__exit__(*args, **kwargs)
