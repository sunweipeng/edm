#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from service.busi_base_conf_service import BusiBaseConfService
from config import busi_config
from util.verify_email_helper import VerifyEmailHelper


class CheckSmtpObserver(Observer):
	"""
	队列检查
	"""
	def update(self):
		result = self.subject.email_list
		self.logger.info("【数据提取】2、队列邮箱有效性检查")
		"""是否校验账号有效性"""
		verify_send_email_smtp = BusiBaseConfService().search_key_return_value((busi_config.VERIFY_SEND_EMAIL_SMTP), "0")
		"""校验有效性标志是否开启"""
		if verify_send_email_smtp == "0":
			return
		verify_email = BusiBaseConfService().search_key_return_value((busi_config.VERIFY_EMAIL))
		"""账号有效性检查"""
		for item in result:
			"""判断是否还有状态字段 存在则无需再次校验 反之则校验"""
			status = item.get("status")
			if status:
				continue
			email = item.get("email")
			"""校验有效性"""
			if self.verify_email_smtp(email, verify_email):
				item["status"] = "1"




	def verify_email_smtp(self, email, verify_email):
		"""
		校验邮箱有效性
		:param email:
		:param verify_email:
		:return:
		"""
		"""校验有效性 0 为无效地址"""
		verify_result_status = VerifyEmailHelper().verify_email(email, verify_email)
		self.logger.info("验证状态为：%s" % str(verify_result_status))
		if verify_result_status == 0:
			return True
		return False


