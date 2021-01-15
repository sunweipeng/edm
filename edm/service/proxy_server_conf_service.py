#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import proxy_server_conf_sql
from util.mysql_helper import MySqlHelper
from base.user_logger import UserLogger
import traceback


class ProxyServerConfService(object):
	"""
	代理服务器
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询代理服务器
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询代理服务器】请求参数为为空，流程结束")
				return False
			#self.logger.info("【查询代理服务器】请求参数为：%s" % param)
			_db = MySqlHelper()
			result = _db.fetch_all(proxy_server_conf_sql.search, param)
			#self.logger.info("【查询代理服务器】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询代理服务器】查询异常信息为：%s" % traceback.format_exc())
		return False

	def update(self, param):
		"""
		更新代理服务器
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新代理服务器】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(proxy_server_conf_sql.update, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新代理服务器】更新异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	pass
