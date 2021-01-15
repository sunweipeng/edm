#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import return_code_conf_sql
from util.mysql_helper import MySqlHelper
from base.user_logger import UserLogger
import traceback

class ReturnCodeConfService(object):
	"""
	返回码配置
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param=None):
		"""
		查询返回码配置
		:return:
		"""
		try:
			#self.logger.info("【查询返回码配置】请求参数为：%s" % param)
			_db = MySqlHelper()
			result = _db.fetch_all(return_code_conf_sql.search, param)
			#self.logger.info("【查询返回码配置】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询返回码配置】查询异常信息为：%s" % traceback.format_exc())
		return False

	def search_key(self, param):
		"""
		查询返回码配置 通过retCode
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询返回码配置】请求参数为为空，流程结束")
				return False
			#self.logger.info("【查询返回码配置】请求参数为：%s" % param)
			_db = MySqlHelper()
			result = _db.fetch_all(return_code_conf_sql.search_by_ret_code, param)
			#self.logger.info("【查询返回码配置】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询返回码配置】查询异常信息为：%s" % traceback.format_exc())
		return False

	def update_by_policy(self, sql):
		"""
		通过策略更新对应数据
		:param sql:
		:return:
		"""
		_db = None
		try:
			if not sql:
				self.logger.info("【更新策略】请求参数为为空，流程结束")
			_db = MySqlHelper()
			"""判断是更新还是插入"""
			if sql.upper().find("INSERT"):
				result = _db.insert_one(sql)
			else:
				result = _db.update(sql)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新策略】保存异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	pass
