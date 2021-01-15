#!/usr/bin/python3
# -*- coding: utf-8 -*-
import queue
from base.user_logger import UserLogger
from base.queueManager import QueueManager



class QueueManagerHelper(object):
	"""
	分布式队列相关帮助
	"""

	def __init__(self, host, key, register_name, is_master=True, port=5000):
		"""
		分布式队列初始化
		:param host:
		:param key:
		:param register_name:
		:param is_master:
		:param port:
		"""
		self.logger = UserLogger.getlog()
		self._host = host
		self._port = port
		self._key = key.encode()
		self._is_master = is_master
		self._register_name = register_name
		self._server = self._get_queue_server()

	@property
	def server(self):
		"""
		获取对象
		:return:
		"""
		return self._server


	def register_queue_index(self, queue_name, queue_list, index):
		"""
		注册方法名
		:param queue_name:
		:param queue_list:
		:param index:
		:return:
		"""
		QueueManager.register(queue_name, callable=lambda: queue_list[index])


	def register_queue(self):
		"""
		注册方法名
		:return:
		"""
		if not isinstance(self._register_name, list):
			"""判断传入参数是否为list"""
			return False
		"""声明队列"""
		queue_list = []
		[queue_list.append(queue.Queue()) for item in self._register_name]
		for index in range(len(self._register_name)):
			"""注册方法名"""
			if self._is_master:
				self.register_queue_index(self._register_name[index], queue_list, index)
			else:
				QueueManager.register(self._register_name[index])
		return True


	def _get_queue_server(self):
		"""
		初始化队列
		:return:
		"""
		"""注册方法"""
		self.register_queue()
		"""建立连接"""
		manager = QueueManager(address=(self._host, self._port), authkey=self._key)
		return manager


	def master_start(self):
		"""
		启动queue 主
		:return:
		"""
		if not isinstance(self._server, QueueManager):
			return False
		self._server.start()


	def worker_start(self):
		"""
		启动queue 从
		:return:
		"""
		if not isinstance(self._server, QueueManager):
			return False
		self._server.connect()


	def queue_close(self):
		"""
		关闭queue
		:return:
		"""
		if not isinstance(self._server, QueueManager):
			return False
		self._server.shutdown()


