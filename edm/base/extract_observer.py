#!/usr/bin/python3
# -*- coding: utf-8 -*

from base.observer import Observer
from base.user_logger import UserLogger


class ExtractObserver(Observer):
	"""
	观察者
	"""
	def __init__(self, subject):
		self.subject = subject
		self.logger = UserLogger.getlog()


	def update(self):
		pass
