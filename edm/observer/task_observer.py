#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from util.redis_helper import RedisHelper


class TaskObserver(Observer):
	"""
	PUSH任务队列
	"""
	def update(self):
		"""
		push任务队列
		:return:
		"""
		result = self.subject.email_list
		rel_id = self.subject.rel_id
		self.logger.info("【数据提取】4、PUSH任务队列")
		for item in result:
			status = item.get("status")
			"""判断状态 如果是黑名单 或者地址无效"""
			if status == "4" or status == "1":
				continue
			level = item.get("level", "1")
			originalBatchCode = item.get("originalBatchCode")
			channel = "%s_%s_pagoda_%s" % (originalBatchCode, rel_id, level)
			RedisHelper().lpush_item(item, channel)



