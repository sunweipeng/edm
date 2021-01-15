#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from base.user_logger import UserLogger


class Observer(ABC):
	"""
	观察者
	"""
	def __init__(self, subject):
		self.subject = subject
		self.logger = UserLogger.getlog()

	@abstractmethod
	def update(self):
		pass
