#!/usr/bin/python3
# -*- coding: utf-8 -*-
import traceback
from base.observer import Observer
from service.pop_record_service import POPRecordService
from util.pop3_util import POP3Util


class POP3RecordObserver(Observer):
	"""
	收取记录入库
	"""
	def update(self):
		"""
		收取记录入库
		:return:
		"""
		result = self.subject.pop3_result
		if not result:
			return
		"""循环添加状态"""
		for item in result:
			status = self.set_record_status(item.get("sendResult", ""))
			item["status"] = status
		flag = POPRecordService().insert_format(result)
		if flag:
			self.logger.info("【收取邮件】收取邮件信息入库完成，删除邮件")
			self.del_email(self.subject.pop3_account)


	def set_record_status(self, text):
		"""
		判断状态
		:param text:
		:return:
		"""
		if text.find("接收地址不存在") > -1 or text.find("无法找到") > -1 or text.find("邮件被退回了") > -1:
			"""地址不存在 不会重新发送"""
			status = 1
		elif text.find("反垃圾系统") > -1 or text.find("发生临时性错误") > -1 or text.find("收件方地址不存在，或暂时不可用") > -1:
			"""地址暂时不可用 可重复发送"""
			status = 2
		else:
			status = 0
		return status


	def del_email(self, result):
		"""
		删除邮件
		:param result:
		:return:
		"""
		try:
			pop3_server = POP3Util(result)
			pop3_server.del_email(result.get("userName"))
		except Exception as e:
			self.logger.info("【收取邮件】删除邮件列表失败，信息为：%s" % traceback.format_exc())


