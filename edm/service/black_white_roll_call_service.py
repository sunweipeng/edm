#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import black_white_roll_call_sql
from util.mysql_helper import MySqlHelper
import traceback
from base.user_logger import UserLogger

class BlackWhiteRollCallService(object):
	"""
	黑白名单配置
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询黑白名单
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询黑白名单】请求参数为为空，流程结束")
				return False
			self.logger.info("【查询黑白名单】请求参数为：%s" % param)
			_db = MySqlHelper()
			result = _db.fetch_all(black_white_roll_call_sql.search, param)
			self.logger.info("【查询黑白名单】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询黑白名单】查询异常信息为：%s" % traceback.format_exc())
		return False

	def search_key(self, param):
		"""
		查询黑白名单 通过content
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询黑白名单】请求参数为为空，流程结束")
				return False
			self.logger.info("【查询黑白名单】请求参数为：%s" % param)
			_db = MySqlHelper()
			result = _db.fetch_all(black_white_roll_call_sql.search_key, param)
			self.logger.info("【查询黑白名单】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询黑白名单】查询异常信息为：%s" % traceback.format_exc())
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
				self.logger.info("【保存黑白名单】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(black_white_roll_call_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存黑白名单】保存异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	pass
