#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import server_conf_sql
from util.mysql_helper import MySqlHelper
from util.business_util import BusinessUtil
from config import busi_config
import traceback
from base.user_logger import UserLogger
import json


class ServerConfService(object):
	"""
	服务器配置相关接口
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()


	def search(self, param=None):
		"""
		查询有效服务器数据 优先查询redis内数据，未查得后查询数据库数据并更新到redis内
		:param param:
		:return: result
		"""
		try:
			result = BusinessUtil.get_redis_by_key(busi_config.SERVER_CONFIG_REDIS_KEY)
			if result:
				return json.loads(result)
			_db = MySqlHelper()
			result = _db.fetch_all(server_conf_sql.search, param)
			if not result:
				self.logger.info("【查询有效服务器】响应结果为空，结束流程")
				return False
			BusinessUtil.set_redis_by_key(busi_config.SERVER_CONFIG_REDIS_KEY, result, busi_config.REDIS_CACHE_TIME)
			return result
		except Exception as e:
			self.logger.error("【查询有效服务器】查询异常信息为：%s" % traceback.format_exc())
		return False

	def update(self, param=None):
		"""
		更新数据
		:param param:
		:return:
		"""
		_db = None
		try:
			BusinessUtil.delete_redis_by_key(busi_config.SERVER_CONFIG_REDIS_KEY)
			if param is None:
				self.logger.info("【更新服务器】请求参数为空，流程结束")
				return False
			_db = MySqlHelper()
			_db.begin()
			count = _db.update(server_conf_sql.update, param)
			_db.end()
			return count
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新服务器】更新异常，事务回滚，异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == '__main__':
	ServerConfService().search()



