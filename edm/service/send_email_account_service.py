#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mapper import send_email_account_sql
from util.mysql_helper import MySqlHelper
import traceback
import time
from base.user_logger import UserLogger
from util.business_util import BusinessUtil
from config import busi_config
import json


class SendEmailAccountService(object):
	"""
	发送邮箱账号
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()

	def search(self, param=None):
		"""
		查询发送有效账号
		:return:
		"""
		try:
			_db = MySqlHelper()
			result = _db.fetch_all(send_email_account_sql.search, param)
			return result
		except Exception as e:
			self.logger.error("【查询发送邮箱账号】查询异常信息为：%s" % traceback.format_exc())
		return False

	def search_not_lock_user_name(self, user_name):
		"""
		查询账号状态
		:param user_name:
		:return:
		"""
		try:
			if not user_name:
				return False
			"""查询数据库"""
			_db = MySqlHelper()
			result = _db.count(send_email_account_sql.search_lock_user_name, user_name)
			"""没有查到数据为空"""
			if not result:
				return True
		except Exception as e:
			self.logger.error("【查询发送邮箱账号】查询异常信息为：%s" % traceback.format_exc())
		return False



	def search_lock_domain_name(self):
		"""
		查询域名状态
		:return:
		"""
		try:
			"""查询redis"""
			result = BusinessUtil.get_redis_by_key(busi_config.LOCK_ACCOUNT_REDIS_KEY)
			if result:
				return result
			"""查询数据库"""
			_db = MySqlHelper()
			result = _db.fetch_one(send_email_account_sql.search_lock_domain_name)
			if not result:
				return False
			"""获取域名"""
			domain_name = result.get("domainName", "")
			"""如果不为空 则添加到redis"""
			if domain_name:
				BusinessUtil.set_redis_by_key(busi_config.LOCK_ACCOUNT_REDIS_KEY, domain_name, busi_config.REDIS_CACHE_TIME)
			return domain_name
		except Exception as e:
			self.logger.error("【查询发送邮箱账号】查询异常信息为：%s" % traceback.format_exc())
		return False



	def search_valid_account(self, server_ip):
		"""
		查询发送有效账号(含剩余数量)
		缓存5分钟 可能存在账号多发情况
		:param server_ip:
		:return:
		"""
		try:
			if not server_ip:
				self.logger.info("【查询发送邮箱账号】传入参数有误，请确认")
				return False
			"""选取发送账号"""
			valid_account_key = "%s_%s" % (server_ip.replace(".", "_"), busi_config.VALID_ACCOUNT_REDIS_KEY)
			"""查询redis"""
			result = BusinessUtil.get_redis_by_key(valid_account_key)
			if not result:
				"""查询数据库"""
				_db = MySqlHelper()
				"""设置当前日期"""
				timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
				start = "%s 00:00:00" % timeStr
				end = "%s 23:59:59" % timeStr
				result = _db.fetch_all(send_email_account_sql.search_valid_account, (server_ip, start, end))
			else:
				"""转化数据"""
				result = json.loads(result)
			"""判断非空"""
			if not result:
				return False
			BusinessUtil.set_redis_by_key(valid_account_key, result, busi_config.REDIS_CACHE_TIME)
			return result
		except Exception as e:
			self.logger.error("【查询发送邮箱账号】查询异常信息为：%s" % traceback.format_exc())
		return False


	def update_all_status_valid(self):
		"""
		更新所有账号为有效
		:return:
		"""
		_db = None
		try:
			_db = MySqlHelper()
			"""更新当前账号 将所有数据转化为1"""
			_db.update(send_email_account_sql.update_all_status_valid)
			_db.end()
			return True
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【变更轮换账号】变更异常信息为：%s" % traceback.format_exc())
		return False




	def search_and_update_account(self, server_ip, account_reopen_time):
		"""
		变更轮换账号
		:param server_ip:
		:param account_reopen_time:
		:return:
		"""
		_db = None
		try:
			_db = MySqlHelper()
			"""设置当前日期"""
			timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			# start = "%s 00:00:00" % timeStr
			# end = "%s 23:59:59" % timeStr
			#result = _db.fetch_all(send_email_account_sql.search_and_update_account, (server_ip, start, end))
			"""更新当前账号 将所有数据转化为3"""
			#_db.update(send_email_account_sql.update_status, (3, 1, server_ip))
			"""查询锁定账号"""
			result = _db.fetch_all(send_email_account_sql.search_lock_account_for_user_name, (timeStr, account_reopen_time, timeStr))
			# if not result:
			# 	"""查询锁定账号"""
			# 	result = _db.fetch_all(send_email_account_sql.search_lock_account, (timeStr, account_reopen_time))
			"""存在数据 则更新"""
			if result:
				for item in result:
					_db.update(send_email_account_sql.update_user_name, (1, item.get("userName")))
			_db.end()
			return True
		except Exception as e:
			if _db:
				_db.isEnd = 2
				_db.end()
			self.logger.error("【变更轮换账号】变更异常信息为：%s" % traceback.format_exc())
		return False



	def search_has_valid_account(self, server_ip):
		"""
		查询待转化的邮箱域名
		:param server_ip:
		:return:
		"""
		_db = None
		try:
			_db = MySqlHelper()
			"""设置当前日期"""
			timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			start = "%s 00:00:00" % timeStr
			end = "%s 23:59:59" % timeStr
			result = _db.fetch_all(send_email_account_sql.search_and_update_account, (server_ip, start, end))
			return result
		except Exception as e:
			self.logger.error("【查询待转化的邮箱域名】查询待转化的邮箱域名信息为：%s" % traceback.format_exc())
		return False


	def search_lock_account(self, account_reopen_time):
		"""
		查询锁定的账号(未达到最大量数据)
		:param account_reopen_time:
		:return:
		"""
		_db = None
		try:
			_db = MySqlHelper()
			"""设置当前日期"""
			timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			result = _db.fetch_all(send_email_account_sql.search_lock_account_for_user_name, (timeStr, account_reopen_time, timeStr))
			return result
		except Exception as e:
			self.logger.error("【查询锁定的账号】查询锁定的账号异常，信息为：%s" % traceback.format_exc())
		return False




	def search_pop(self, param=None):
		"""
		查询发送有效账号 POP
		:return:
		"""
		try:
			_db = MySqlHelper()
			result = _db.fetch_all(send_email_account_sql.search_pop, param)
			return result
		except Exception as e:
			self.logger.error("【查询发送邮箱账号】查询异常信息为：%s" % traceback.format_exc())
		return False


	def search_pop_server_ip(self, server_ip):
		"""
		通过服务ip查询账号
		:param server_ip:
		:return:
		"""
		try:
			if not server_ip:
				return False
			_db = MySqlHelper()
			result = _db.fetch_all(send_email_account_sql.search_pop_server_ip, server_ip)
			return result
		except Exception as e:
			self.logger.error("【查询发送邮箱账号】查询异常信息为：%s" % traceback.format_exc())
		return False



	def search_smtp(self, param=None):
		"""
		查询发送有效账号 SMTP
		:return:
		"""
		try:
			_db = MySqlHelper()
			result = _db.fetch_all(send_email_account_sql.search_smtp, param)
			return result
		except Exception as e:
			self.logger.error("【查询发送邮箱账号】查询异常信息为：%s" % traceback.format_exc())
		return False


	def update(self, param):
		"""
		更新发送邮箱账号
		:return:
		"""
		_db = None
		try:
			if not param:
				self.logger.info("【更新发送邮箱账号】请求参数为为空，流程结束")
				return False
			_db = MySqlHelper()
			result = _db.insert_one(send_email_account_sql.update, param)
			_db.end()
			return result
		except Exception as e:
			_db.isEnd = 2
			_db.end()
			self.logger.error("【更新发送邮箱账号】更新异常信息为：%s" % traceback.format_exc())
		return False



if __name__ == "__main__":
	from base import global_argument
	global_argument.set_value("106.12.219.104")
	print(SendEmailAccountService().search_lock_user_name("mxf_m1@m7bee.cn"))
