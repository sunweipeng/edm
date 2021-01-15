#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import email_address_book_sql
from util.mysql_helper import MySqlHelper
from base.user_logger import UserLogger
import traceback


class EmailAddressBookService(object):
	"""
	通讯录
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询通讯录
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询通讯录】请求参数为为空，流程结束")
				return False
			self.logger.info("【查询通讯录】请求参数为：%s" % param)
			_db = MySqlHelper()
			result = _db.fetch_all(email_address_book_sql.search, param)
			self.logger.info("【查询通讯录】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询通讯录】查询异常信息为：%s" % traceback.format_exc())
		return False

	def update(self, param):
		"""
		更新通讯录
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新通讯录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(email_address_book_sql.update, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新通讯录】更新异常信息为：%s" % traceback.format_exc())
		return False


	def insert(self, param):
		"""
		添加数据
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存通讯录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(email_address_book_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存通讯录】保存异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	pass
