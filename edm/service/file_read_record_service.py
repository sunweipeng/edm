#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import file_read_record_sql
from util.mysql_helper import MySqlHelper
from util.business_util import BusinessUtil
import traceback
from base.user_logger import UserLogger
import json


class FileReadRecordService(object):
	"""
	文件读取相关记录
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()


	def search(self, param):
		"""
		文件读取相关记录
		:param param:
		:return:
		"""
		try:
			_db = MySqlHelper()
			result = _db.fetch_all(file_read_record_sql.search, param)
			if not result:
				self.logger.info("【文件读取记录】响应结果为空，结束流程")
				return False
			return result
		except Exception as e:
			self.logger.error("【文件读取记录】查询异常信息为：%s" % traceback.format_exc())
		return False



	def insert(self, param):
		"""
		文件读取记录添加
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【文件读取记录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(file_read_record_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【文件读取记录】保存异常信息为：%s" % traceback.format_exc())
		return False



	def update(self, param=None):
		"""
		文件读取记录更新
		:param param:
		:return:
		"""
		_db = None
		try:
			_db = MySqlHelper()
			_db.begin()
			count = _db.update(file_read_record_sql.update, param)
			_db.end()
			return count
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【文件读取记录】更新异常，事务回滚，异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	pass
