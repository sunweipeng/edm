#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from service.send_record_service import SendRecordService



class SendRecordObserver(Observer):
	"""
	投递记录入库
	"""
	def update(self):
		"""
		投递记录入库
		:return:
		"""
		self.logger.info("【发送邮件】4、投递记录开始入库")
		result = self.subject.email_item
		SendRecordService().insert((result.get("batchCode"), result.get("subBatchCode"), result.get("mobile"), result.get("email"), result.get("templateExtCode"), result.get("serverIp"), result.get("userName"), int(result.get("send_status"))))








