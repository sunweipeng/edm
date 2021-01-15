#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import primary_data_sql
from util.mysql_helper import MySqlHelper
import traceback
from base.user_logger import UserLogger


class PrimaryDataService(object):

	"""
	原始营销数据
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询原始营销数据
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询原始营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.fetch_all(primary_data_sql.search, param)
			return result
		except Exception as e:
			self.logger.error("【查询原始营销数据】查询异常信息为：%s" % traceback.format_exc())
		return False

	def update(self, param):
		"""
		更新原始营销数据
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新原始营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.update(primary_data_sql.update, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新原始营销数据】更新异常信息为：%s" % traceback.format_exc())
		return False

	def update_roll_back(self, param):
		"""
		回退数据
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【回退原始营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.update(primary_data_sql.update_roll_back, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【回退原始营销数据】更新异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	PrimaryDataService().search((1))
