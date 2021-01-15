#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from service.marketing_data_service import MarketingDataService
from exception.business_exception import BusinessExcetion


class MarketingObserver(Observer):
	"""
	营销数据入库
	"""
	def update(self):
		"""
		营销数据入库
		:return:
		"""
		result = self.subject.email_list
		self.logger.info("【数据提取】3、营销数据入库：%s" % len(result))
		if not result:
			return
		"""执行入库/更新操作  异常回滚"""
		flag = MarketingDataService().insert_update_more(result)
		if not flag:
			raise BusinessExcetion("T03", "营销数据回滚")




