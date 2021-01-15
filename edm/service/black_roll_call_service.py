#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import black_roll_call_sql
from util.mysql_helper import MySqlHelper
import traceback
from base.user_logger import UserLogger
from util.business_util import BusinessUtil


class BlackRollCallService(object):
	"""
	黑名单配置
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询黑名单
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询黑名单】请求参数为为空，流程结束")
				return False
			self.logger.info("【查询黑名单】请求参数为：%s" % param)
			_db = MySqlHelper()
			result = _db.fetch_all(black_roll_call_sql.search, param)
			self.logger.info("【查询黑名单】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询黑名单】查询异常信息为：%s" % traceback.format_exc())
		return False


	def search_key(self, param):
		"""
		查询黑名单 通过content
		:return:
		"""
		try:
			if not param:
				return False
			"""从redis读取字段"""
			result = BusinessUtil.get_redis_by_key(param)
			if result:
				return result
			"""从数据库内查询"""
			_db = MySqlHelper()
			result = _db.fetch_all(black_roll_call_sql.search_key)
			"""未查到数据"""
			if not result:
				return False
			black_dict = {}
			"""循环遍历数据"""
			for item in result:
				if not item:
					continue
				"""生成分组"""
				item_key = BusinessUtil.get_verify_key(item.get("content"))
				if not item_key:
					continue
				if item_key in black_dict:
					black_dict[item_key].append(item.get("content"))
				else:
					black_dict.setdefault(item_key, [])
					black_dict[item_key].append(item.get("content"))
			"""存入redis"""
			result_str = None
			for key in list(black_dict.keys()):
				item = black_dict[key]
				item_list = list(set(item))
				item_str = ",".join(item_list)
				if key == param:
					result_str = item_str
				BusinessUtil.set_redis_reset_time_ex(key, item_str)
			return result_str
		except Exception as e:
			self.logger.error("【查询黑名单】查询异常信息为：%s" % traceback.format_exc())
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
				self.logger.info("【保存黑名单】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(black_roll_call_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存黑名单】保存异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	BlackRollCallService().search_key("123142_verify")
	pass
