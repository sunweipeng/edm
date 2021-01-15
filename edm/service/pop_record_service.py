#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import pop_record_sql
from util.mysql_helper import MySqlHelper
from base.user_logger import UserLogger
import traceback


class POPRecordService(object):
	"""
	收取记录
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询收取记录
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询收取记录】请求参数为为空，流程结束")
				return False
			#self.logger.info("【查询收取记录】请求参数为：%s" % param)
			_db = MySqlHelper()
			result = _db.fetch_all(pop_record_sql.search, param)
			#self.logger.info("【查询收取记录】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询收取记录】查询异常信息为：%s" % traceback.format_exc())
		return False

	def update(self, param):
		"""
		更新收取记录
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新收取记录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(pop_record_sql.update, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新收取记录】更新异常信息为：%s" % traceback.format_exc())
		return False


	def insert(self, param):
		"""
		添加收取记录
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存收取记录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(pop_record_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存收取记录】保存异常信息为：%s" % traceback.format_exc())
		return False


	def insert_more(self, param):
		"""
		添加收取记录
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存收取记录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_more(pop_record_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存收取记录】保存异常信息为：%s" % traceback.format_exc())
		return False

	def insert_format(self, result):
		"""
		添加收取记录
		:param result:
		:return:
		"""
		_db = None
		try:
			if not result:
				self.logger.info("【保存收取记录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			for item in result:
				insert_format = pop_record_sql.insert_format.format(**item)
				_db.insert_one(insert_format)
			_db.end()
			return True
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存收取记录】保存异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	pass
