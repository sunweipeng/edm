#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from DBUtils.PersistentDB import PersistentDB
from config import db_config
from base import global_argument

sql_settings = db_config.mysql_config


'''mysql 工具类'''
class MySqlHelper(object):
	__pool = None
	__con = None

	def __init__(self, pooled=True):
		"""
		初始
		:param pooled:
		"""
		self._conn = MySqlHelper.__get_conn(pooled)
		self._cursor = self._conn.cursor()
		self._isEnd = 1

	@property
	def isEnd(self):
		"""
		get
		:return:
		"""
		return self._isEnd

	@isEnd.setter
	def isEnd(self, value):
		"""
		set
		:param value:
		:return:
		"""
		self._isEnd = value

	@classmethod
	def __get_conn(cls, pooled=True):
		"""
		获取数据库链接
		:param pooled:
		:return:
		"""
		"""获取公网IP"""
		public_ip = global_argument.get_value()
		"""更新host值"""
		if public_ip == sql_settings.get("host"):
			sql_settings["host"] = "127.0.0.1"

		if pooled:
			if MySqlHelper.__pool is None:
				MySqlHelper.__pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, use_unicode=True, cursorclass=DictCursor, **sql_settings)
			return MySqlHelper.__pool.connection()
		else:
			if MySqlHelper.__con is None:
				MySqlHelper.__con = PersistentDB(pymysql, cursorclass=DictCursor, **sql_settings).connection()
			return MySqlHelper.__con

	def __del__(self):
		"""
		回收关闭链接
		:return:
		"""
		self.close()

	def __query(self, sql, param):
		"""
		查询/添加
		:param sql:
		:param param:
		:return:
		"""
		if param is None:
			count = self._cursor.execute(sql)
		else:
			count = self._cursor.execute(sql, param)
		return count


	def insert_more(self, sql, values):
		"""
		插入多条数据
		:param sql:
		:param values:
		:return:
		"""
		return self._cursor.executemany(sql, values)

	'''insert one'''
	def insert_one(self, sql, value=None):
		"""
		插入一条数据
		:param sql: 使用(%s,%s)
		:param value: 值 tuple/list
		:return:
		"""
		return self.__query(sql, value)


	def delete(self, sql, param=None):
		"""
		删除数据
		:param sql:
		:param param:
		:return:
		"""
		return self.__query(sql, param)


	def update(self, sql, param=None):
		"""
		更新数据
		:param sql:
		:param param:
		:return:
		"""
		return self.__query(sql, param)


	def count(self, sql, param=None):
		"""
		查询条数
		:param sql:
		:param param:
		:return:
		"""
		return self.__query(sql, param)


	def fetch_all(self, sql, param=None):
		"""
		查询全部数据
		:param sql:
		:param param:
		:return:
		"""
		count = self.__query(sql, param)
		if count > 0:
			result = self._cursor.fetchall()
		else:
			result = False
		return result

	def fetch_one(self, sql, param=None):
		"""
		查询一条数据
		:param sql:
		:param param:
		:return:
		"""
		count = self.__query(sql, param)
		if count > 0:
			result = self._cursor.fetchone()
		else:
			result = False
		return result

	def fetch_many(self, sql, num, param=None):
		"""
		查询全部
		:param sql:
		:param num:
		:param param:
		:return:
		"""
		count = self.__query(sql, param)
		if count > 0:
			result = self._cursor.fetchmany(num)
		else:
			result = False
		return result

	def begin(self):
		"""
		开启事务
		:return:
		"""
		pass
		#self._conn.autocommit(0)

	def end(self, option='commit'):
		"""
		结束
		:param option:
		:return:
		"""
		if option == 'commit':
			self._conn.commit()
		else:
			self._conn.rollback()

	def close(self):
		"""
		关闭连接
		:param isEnd:
		:return:
		"""
		if self._isEnd == 1:
			self.end('commit')
		else:
			self.end('rollback')
		if self._cursor:
			self._cursor.close()
		if self._conn:
			self._conn.close()

