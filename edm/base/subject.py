#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Subject(ABC):
	observers = None
	email_list = None
	email_item = None
	pop3_result = None
	pop3_account = None
	account_list = None
	rel_id = None

	"""
	被观察者
	"""
	def __init__(self):
		pass

	@abstractmethod
	def attach(self, observer):
		pass

	@abstractmethod
	def detach(self, observer):
		pass

	@abstractmethod
	def notify(self):
		pass
