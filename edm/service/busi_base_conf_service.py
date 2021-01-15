#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import busi_base_conf_sql
from util.mysql_helper import MySqlHelper
import traceback
from base.user_logger import UserLogger
from util.business_util import BusinessUtil
from config import busi_config
import json


class BusiBaseConfService(object):
	"""
	查询业务配置
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param=None):
		"""
		查询业务配置 通过状态
		:return:
		"""
		try:
			_db = MySqlHelper()
			result = _db.fetch_all(busi_base_conf_sql.search, param)
			return result
		except Exception as e:
			self.logger.error("【查询业务配置】查询异常信息为：%s" % traceback.format_exc())
		return False

	def search_key(self, param):
		"""
		查询业务配置  通过key值
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询业务配置】请求参数为为空，流程结束")
				return False
			"""查询redis"""
			result = BusinessUtil.get_redis_by_key(busi_config.BUSI_BASE_CONF_REDIS_KEY)
			if not result:
				"""查询数据库"""
				_db = MySqlHelper()
				result = _db.fetch_all(busi_base_conf_sql.search, None)
			else:
				"""转化数据"""
				result = json.loads(result)
			"""存储到redis"""
			BusinessUtil.set_redis_by_key(busi_config.BUSI_BASE_CONF_REDIS_KEY, result, busi_config.REDIS_CACHE_TIME)
			"""遍历结果"""
			busi_base_list = []
			for item in result:
				if item.get("busiKey") != param:
					continue
				busi_base_list.append(item)
				break
			if not busi_base_list:
				return False
			return busi_base_list[0]
		except Exception as e:
			self.logger.error("【查询业务配置】查询异常信息为：%s" % traceback.format_exc())
		return False


	def search_key_return_value(self, param, default_value=""):
		"""
		查询业务配置  通过key值
		:param param:
		:param default_value:
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询业务配置】请求参数为为空，流程结束")
				return False
			"""查询redis"""
			result = BusinessUtil.get_redis_by_key(busi_config.BUSI_BASE_CONF_REDIS_KEY)
			if not result:
				"""查询数据库"""
				_db = MySqlHelper()
				result = _db.fetch_all(busi_base_conf_sql.search, None)
			else:
				"""转化数据"""
				result = json.loads(result)
			"""存储到redis"""
			BusinessUtil.set_redis_by_key(busi_config.BUSI_BASE_CONF_REDIS_KEY, result, busi_config.REDIS_CACHE_TIME)
			"""遍历结果"""
			busi_base_list = []
			for item in result:
				if item.get("busiKey") != param:
					continue
				busi_base_list.append(item)
				break
			if not busi_base_list:
				return False
			return busi_base_list[0].get("busiValue", default_value)
		except Exception as e:
			self.logger.error("【查询业务配置】查询异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	basi_conf = BusiBaseConfService().search_key_return_value((busi_config.RESEND_RULES),'1|1|1')
	print(basi_conf)
