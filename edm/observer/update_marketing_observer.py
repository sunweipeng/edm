#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from service.marketing_data_service import MarketingDataService



class UpdateMarketingObserver(Observer):
	"""
	更新营销数据
	"""
	def update(self):
		"""
		更新营销数据
		:return:
		"""
		result = self.subject.pop3_result
		if not result:
			return
		for item in result:
			"""更新营销数据"""
			self.update_marketing_data(item)


	def update_marketing_data(self, item):
		"""
		更新数据
		:param item:
		:return:
		"""
		email = item.get("email", "")
		status = int(item.get("status", "0"))
		sendResult = item.get("sendResult", "")
		MarketingDataService().update((status, sendResult, email))


