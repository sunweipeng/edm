#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging.config
import os


class UserLogger(object):

	def __init__(self):
		pass

	@staticmethod
	def getlog():
		"""
		基础日志
		:return:
		"""
		basePath = os.path.dirname(os.path.realpath(__file__)).replace("base", "")
		logging.config.fileConfig('%s/config/logging.conf' % basePath)
		return logging.getLogger('detail')



