#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import marketing_data_sql
from util.mysql_helper import MySqlHelper
from base.user_logger import UserLogger
from util.business_util import BusinessUtil
import traceback



class MarketingDataService(object):

	"""
	营销数据
	"""
	def __init__(self):
		# log日志
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询营销数据
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.fetch_all(marketing_data_sql.search, param)
			return result
		except Exception as e:
			self.logger.error("【查询营销数据】查询异常信息为：%s" % traceback.format_exc())
		return False

	def update(self, param):
		"""
		更新营销数据
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.update(marketing_data_sql.update, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新营销数据】更新异常信息为：%s" % traceback.format_exc())
		return False

	def update_status(self, param):
		"""
		更新营销数据
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.update(marketing_data_sql.update_status, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新营销数据】更新异常信息为：%s" % traceback.format_exc())
		return False


	def insert(self, param):
		"""
		添加营销数据
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(marketing_data_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存营销数据】保存异常信息为：%s" % traceback.format_exc())
		return False


	def insert_more(self, param):
		"""
		添加营销数据
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_more(marketing_data_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存营销数据】保存异常信息为：%s" % traceback.format_exc())
		return False

	def insert_update(self, param):
		"""
		添加或更新数据
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【添加/更新营销数据】请求参数为为空，流程结束")
			"""查询数据"""
			_db = MySqlHelper()
			count = _db.count(marketing_data_sql.count, (param.get("batchCode"), param.get("mobile"), param.get("email")))
			if count > 0:
				result = _db.update(marketing_data_sql.update_insert, (param.get("subBatchCode"), param.get("batchCode"), param.get("mobile"), param.get("email")))
			else:
				result = _db.insert_one(marketing_data_sql.insert, (param.get("batchCode"), param.get("subBatchCode"), param.get("mobile"), param.get("email")))
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【添加/更新营销数据】保存异常信息为：%s" % traceback.format_exc())
		return False

	def insert_update_more(self, result):
		"""
		添加或更新数据
		:param result:
		:return:
		"""
		_db = None
		try:
			if not result:
				self.logger.info("【添加/更新营销数据】请求参数为为空，流程结束")
			"""查询数据"""
			_db = MySqlHelper()
			for param in result:
				param["subBatchCode"] = BusinessUtil.get_uniqu_time()
				count = _db.count(marketing_data_sql.count, (param.get("batchCode"), param.get("mobile"), param.get("email")))
				if count > 0:
					result = _db.update(marketing_data_sql.update_insert, (
					param.get("subBatchCode"), int(param.get("status", "0")), param.get("batchCode"), param.get("mobile"), param.get("email")))
				else:
					result = _db.insert_one(marketing_data_sql.insert, (
					param.get("originalBatchCode"), param.get("batchCode"), param.get("subBatchCode"), param.get("mobile"), param.get("email"), int(param.get("status", "0"))))
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【添加/更新营销数据】保存异常信息为：%s" % traceback.format_exc())
		return False


	def resend_search(self, param):
		"""
		提取二次营销数据
		:param param:
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询二次营销数据】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.fetch_all(marketing_data_sql.resend_search, param)
			return result
		except Exception as e:
			self.logger.error("【查询二次营销数据】查询异常信息为：%s" % traceback.format_exc())
		return False



if __name__ == "__main__":
	pass
