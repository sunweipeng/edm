#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from service.marketing_data_service import MarketingDataService



class SendEmailUpdateMarketingDataObserver(Observer):
	"""
	更新营销数据
	"""
	def update(self):
		"""
		更新营销数据
		:return:
		"""
		self.logger.info("【发送邮件】5、营销数据开始更新")
		result = self.subject.email_item
		send_status = int(result.get("send_status"))
		if send_status == 1:
			"""判断发送状态 如果发送成功 则状态变更 反之不做处理"""
			MarketingDataService().update_status((3, result.get("batchCode"), result.get("mobile"), result.get("email")))
		else:
			"""更新状态失败"""
			MarketingDataService().update_status((2, result.get("batchCode"), result.get("mobile"), result.get("email")))

