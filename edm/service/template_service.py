#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import template_sql
from util.mysql_helper import MySqlHelper
from util.business_util import BusinessUtil
from config import busi_config
import traceback
from base.user_logger import UserLogger
import json
import random


class TemplateService(object):
	"""
	邮件模板相关接口
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()


	def search_template_code(self, task_code):
		try:
			template_redis_key = "%s_%s" % (task_code, busi_config.TEMPLATE_REDIS_KEY)
			result = BusinessUtil.get_redis_by_key(template_redis_key)
			if not result:
				_db = MySqlHelper()
				result = _db.fetch_all(template_sql.search_template_code, task_code)
				if not result:
					return False
				"""redis入库"""
				BusinessUtil.set_redis_by_key(template_redis_key, result, busi_config.REDIS_CACHE_TIME)
			else:
				if type(result) == str:
					result = json.loads(result)
			"""筛选templateCode"""
			item = random.choice(result)
			return item.get("templateCode")
		except Exception as e:
			self.logger.error("【查询有效服务器】查询异常信息为：%s" % traceback.format_exc())
		return False


	def search(self, task_code):
		"""
		查询有效模板数据
		:param task_code:
		:return:
		"""
		try:
			template_code = self.search_template_code(task_code)
			"""未查到模板编码"""
			if not template_code:
				return False
			"""查询redis"""
			template_redis_key = "%s_%s" % (template_code, busi_config.TEMPLATE_EXT_REDIS_KEY)
			result = BusinessUtil.get_redis_by_key(template_redis_key)
			if result:
				return result
			_db = MySqlHelper()
			result = _db.fetch_all(template_sql.search, template_code)
			"""如果未查到值"""
			if not result:
				return False
			"""redis入库"""
			BusinessUtil.set_redis_by_key(template_redis_key, result, busi_config.REDIS_CACHE_TIME)
			return result
		except Exception as e:
			self.logger.error("【查询有效服务器】查询异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == '__main__':
	from base import global_argument

	global_argument.set_value("106.12.219.104")
	print(TemplateService().search('201905241427196394251011058'))



