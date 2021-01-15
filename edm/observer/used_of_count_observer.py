#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from base.observer import Observer
from service.used_of_count_service import UsedOfCountService



class UsedOfCountObserver(Observer):
	"""
	账号使用量入库
	"""
	def update(self):
		"""
		账号使用量入库
		:return:
		"""
		self.logger.info("【发送邮件】6、账号使用量更新入库")
		result = self.subject.email_item
		send_status = int(result.get("send_status"))
		timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
		start = "%s 00:00:00" % timeStr
		end = "%s 23:59:59" % timeStr
		param = {
			"start": start,
			"end": end,
			"usedOfContent": result.get("userName"),
			"usedType": 2
		}
		"""判断返回码 如果为0 则其他异常，更新"""
		if send_status == 0:
			UsedOfCountService().update_used_subtract(param)
		else:
			UsedOfCountService().insert_update_used(param)

