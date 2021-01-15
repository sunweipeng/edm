#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import send_record_sql
from util.mysql_helper import MySqlHelper
from base.user_logger import UserLogger
import traceback
import time


class SendRecordService(object):
	"""
	发送记录
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param):
		"""
		查询发送记录
		:return:
		"""
		try:
			if not param:
				self.logger.info("【查询发送记录】请求参数为为空，流程结束")
				return False
			self.logger.info("【查询发送记录】请求参数为：%s" % str(param))
			_db = MySqlHelper()
			result = _db.fetch_all(send_record_sql.search, param)
			self.logger.info("【查询发送记录】响应结果为：%s" % result)
			return result
		except Exception as e:
			self.logger.error("【查询发送记录】查询异常信息为：%s" % traceback.format_exc())
		return False


	def search_by_status(self, user_name, status):
		"""
		通过账号、状态查询当前用户发送次数
		:param user_name:
		:param status:
		:return:
		"""
		try:
			"""参数异常"""
			if not user_name or not status:
				return False
			"""查询"""
			timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			_db = MySqlHelper()
			result = _db.fetch_one(send_record_sql.search_by_status, (user_name, status, timeStr))
			if not result:
				return False
			return result.get("num", 0)
		except Exception as e:
			self.logger.error("【查询发送记录】查询异常信息为：%s" % traceback.format_exc())
		return False



	def insert(self, param):
		"""
		添加发送记录
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存发送记录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(send_record_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存发送记录】保存异常信息为：%s" % traceback.format_exc())
		return False


	def insert_more(self, param):
		"""
		添加发送记录
		:param param:
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【保存发送记录】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_more(send_record_sql.insert, param)
			_db.end()
			return result
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【保存发送记录】保存异常信息为：%s" % traceback.format_exc())
		return False


if __name__ == "__main__":
	pass
