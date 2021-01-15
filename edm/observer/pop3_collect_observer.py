#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from util.pop3_util import POP3Util


class POP3CollectObserver(Observer):
	"""
	pop3收取邮件
	"""
	def update(self):
		"""
		pop3收取邮件
		:return:
		"""
		result = self.subject.pop3_account
		self.logger.info("【收取邮件】1、POP3收取邮件，初始账号为：%s" % result.get("userName"))
		"""初始化POP3协议"""
		pop3_server = POP3Util(result)
		"""收取邮件"""
		pop3_result = pop3_server.pop3_email(result.get("userName"))
		self.subject.pop3_result = pop3_result
		self.logger.info("【收取邮件】收取邮件为：%s" % len(pop3_result))


