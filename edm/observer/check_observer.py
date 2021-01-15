#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer


class CheckObserver(Observer):
	"""
	队列检查
	"""
	def update(self):
		self.logger.info("【数据提取】2、队列检查")
		"""开启黑名单校验"""
		"""开启smtp校验"""
		"""自有rcpt校验"""
		"""163注册校验"""




