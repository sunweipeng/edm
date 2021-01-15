#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import used_of_count_sql
from util.mysql_helper import MySqlHelper
from base.user_logger import UserLogger
import traceback
import time



class UsedOfCountService(object):

	"""
	账号使用量统计
	"""
	def __init__(self):
		# log日志
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询账号使用量
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询账号使用量】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.fetch_all(used_of_count_sql.search, param)
			return result
		except Exception as e:
			self.logger.error("【查询账号使用量】查询异常信息为：%s" % traceback.format_exc())
		return False


	def search_account_residue(self, user_name):
		"""
		查询账号剩余量
		:param user_name:
		:return:
		"""
		try:
			if not user_name:
				return False
			timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			_db = MySqlHelper()
			result = _db.fetch_one(used_of_count_sql.search_account_residue, (timeStr, user_name))
			if not result:
				return False
			return result.get("residue", 0)
		except Exception as e:
			self.logger.error("【查询账号使用量】查询异常信息为：%s" % traceback.format_exc())
		return False




	def search_by_type(self, param):
		"""
		查询发送账号信息
		:param param:
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询发送账号信息】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.fetch_all(used_of_count_sql.search_by_type, param)
			return result
		except Exception as e:
			self.logger.error("【查询发送账号信息】查询异常信息为：%s" % traceback.format_exc())
		return False


	def update_used_count(self, param):
		"""
		更新账号使用量
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新账号使用量】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.update(used_of_count_sql.update_used_count, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新账号使用量】更新异常信息为：%s" % traceback.format_exc())
		return False



	def update_select_count(self, param):
		"""
		更新账号使用量
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新账号使用量】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(used_of_count_sql.update_select_count, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【更新账号使用量】更新异常信息为：%s" % traceback.format_exc())
		return False

	def insert(self, param):
		"""
		添加账号使用量
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存账号使用量】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(used_of_count_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存账号使用量】保存异常信息为：%s" % traceback.format_exc())
		return False


	def insert_more(self, param):
		"""
		添加账号使用量
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存账号使用量】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_more(used_of_count_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存账号使用量】保存异常信息为：%s" % traceback.format_exc())
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
				self.logger.info("【添加/更新账号使用量】请求参数为为空，流程结束")
			"""查询数据"""
			_db = MySqlHelper()
			count = _db.count(used_of_count_sql.count, (param.get("usedOfContent"), param.get("usedType"), param.get("start"), param.get("end")))
			if count > 0:
				result = _db.update(used_of_count_sql.update_select_count, (param.get("usedOfContent"), param.get("usedType"), param.get("start"), param.get("end")))
			else:
				result = _db.insert_one(used_of_count_sql.insert, (param.get("usedOfContent"), param.get("usedType")))
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【添加/更新账号使用量】保存异常信息为：%s" % traceback.format_exc())
		return False


	def insert_update_used(self, param):
		"""
		添加或更新数据
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【添加/更新账号使用量】请求参数为为空，流程结束")
			"""查询数据"""
			_db = MySqlHelper()
			count = _db.count(used_of_count_sql.count, (param.get("usedOfContent"), param.get("usedType"), param.get("start"), param.get("end")))
			if count > 0:
				result = _db.update(used_of_count_sql.update_used_count, (param.get("usedOfContent"), param.get("usedType"), param.get("start"), param.get("end")))
			else:
				result = _db.insert_one(used_of_count_sql.insert_used, (param.get("usedOfContent"), param.get("usedType")))
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【添加/更新账号使用量】保存异常信息为：%s" % traceback.format_exc())
		return False


	def update_used_subtract(self, param):
		"""
		更新状态 相减
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【添加/更新账号使用量】请求参数为为空，流程结束")
			"""查询数据"""
			_db = MySqlHelper()
			count = _db.count(used_of_count_sql.count, (param.get("usedOfContent"), param.get("usedType"), param.get("start"), param.get("end")))
			if count <= 0:
				return True
			result = _db.update(used_of_count_sql.update_used_subtract, (param.get("usedOfContent"), param.get("usedType"), param.get("start"), param.get("end")))

			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【添加/更新账号使用量】保存异常信息为：%s" % traceback.format_exc())
		return False




if __name__ == "__main__":
	pass
