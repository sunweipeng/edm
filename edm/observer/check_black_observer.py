#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from service.busi_base_conf_service import BusiBaseConfService
from config import busi_config
from util.business_util import BusinessUtil
from service.black_roll_call_service import BlackRollCallService


class CheckBlackObserver(Observer):
	"""
	队列检查
	"""
	def update(self):
		result = self.subject.email_list
		self.logger.info("【数据提取】1、队列黑名单检查")
		"""是否校验黑名单"""
		verify_black_roll_call = BusiBaseConfService().search_key_return_value((busi_config.VERIFY_BLACK_ROLL_CALL), "0")
		"""黑名单"""
		if verify_black_roll_call == "0":
			return
		for item in result:
			email = item.get("email")
			"""黑名单校验  True 在黑名单内 Flase 不再黑名单内"""
			if self.verify_email_is_in_black_roll_call(email):
				item["status"] = "4"




	def verify_email_is_in_black_roll_call(self, email):
		"""
		校验是否在黑名单内
		:param email:
		:return:
		"""
		"""获取redis key值"""
		redis_key = BusinessUtil.get_verify_key(email)
		"""如果未获取到值"""
		if not redis_key:
			return False
		"""通过key值查询redis"""
		redis_verify_email_value = BlackRollCallService().search_key(redis_key)
		"""未找到值"""
		if not redis_verify_email_value:
			return False
		"""从黑名单内查到字段"""
		if redis_verify_email_value.find(email) > -1:
			return True
		return False



