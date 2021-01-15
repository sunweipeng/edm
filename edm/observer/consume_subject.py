#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.subject import Subject

class ConsumeSubject(Subject):
	"""
	消费
	"""
	def __init__(self):
		self.observers = []

	def attach(self, observer):
		self.observers.append(observer)

	def detach(self, observer):
		self.observers.remove(observer)

	def notify(self):
		for observer in self.observers:
			observer.update()
