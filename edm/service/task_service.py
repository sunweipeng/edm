#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import task_sql
from util.mysql_helper import MySqlHelper
import traceback
from base.user_logger import UserLogger



class TaskService(object):
	"""
	任务类相关接口
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()


	def search_task_code_by_server_ip(self, server_ip):
		"""
		通过服务器IP查询任务编号
		:param server_ip
		:return:
		"""
		try:
			_db = MySqlHelper()
			result = _db.fetch_one(task_sql.search_task_code_by_server_ip, server_ip)
			if not result:
				self.logger.info("【查询任务编号】响应结果为空，结束流程")
				return False
			return result
		except Exception as e:
			self.logger.error("【查询任务编号】查询异常信息为：%s" % traceback.format_exc())
		return False
