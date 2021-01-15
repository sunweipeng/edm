#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import time
import json
import traceback
from base.user_logger import UserLogger
from util.business_util import BusinessUtil
from exception.business_exception import BusinessExcetion
from util.redis_helper import RedisHelper
from observer.tast_queue_subject import TaskQueueSubject
from observer.search_send_account_observer import SearchSendAccountObserver
from observer.search_send_email_content_observer import SearchSendEmailContentObserver
from observer.search_server_ip_observer import SearchServerIpObserver
from concurrent.futures import ThreadPoolExecutor, wait
from config import busi_config
from service.send_email_account_service import SendEmailAccountService
from service.busi_base_conf_service import BusiBaseConfService
from util.kafka_helper import KafkaProducerHelper
from util.queue_manager_helper import QueueManagerHelper
from service.task_service import TaskService
from base import global_argument


class TaskProduct(object):
	"""
	分布式服务进程
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()
		"""当前服务器IP地址"""
		self.public_ip = BusinessUtil.get_public_ip()
		"""设置全局变量"""
		global_argument.set_value(self.public_ip)
		self.task_code = None
		self.relId = None



	def get_task_list(self):
		"""
		获取数据列表 (例：201905241427196394251011058_1_pagoda_1,201905241427196394251011058_2_pagoda_2)
		:return:
		"""
		pattern = "%s_[0-9]*_pagoda_[0-9]*" % self.task_code
		result = BusinessUtil.get_redis_name_by_keys(pattern)
		return result


	def observer(self, result):
		"""
		生成队列信息，确定账号、发送内容、服务器IP
		:param result:
		:return:
		"""
		"""添加当前ip"""
		result["public_ip"] = self.public_ip
		result["task_code"] = self.task_code
		subject = TaskQueueSubject()
		"""1、确定账号"""
		observer1 = SearchSendAccountObserver(subject)
		"""2、确定发送内容"""
		observer2 = SearchSendEmailContentObserver(subject)
		"""3、确定服务器IP"""
		observer3 = SearchServerIpObserver(subject)
		subject.attach(observer1)
		subject.attach(observer2)
		subject.attach(observer3)
		subject.email_item = result
		subject.notify()
		return subject.email_item


	def queue_manager_helper(self, server_dict, queue_length):
		"""
		服务进程启动队列并注册到网络
		:param server_dict:
		:param queue_length:
		:return:
		"""
		manager = None
		try:
			manager = QueueManagerHelper('', busi_config.QUEUE_MANAGER_AUTH_KEY, list(server_dict.keys()))
			manager.master_start()
			"""结果队列"""
			result = manager.server.get_result_queue()
			"""添加任务"""
			for key, value in server_dict.items():
				if not value:
					continue
				task_queue = eval("manager.server.%s" % key)()
				[task_queue.put(item) for item in value]

			self.logger.info("【服务进程】-------------------------浮屠长生 等待响应结果-------------------------")
			"""响应结果"""
			for i in range(queue_length):
				try:
					self.logger.info("服务进程】响应结果为：%s" % result.get(timeout=10))
				except Exception as e:
					self.logger.error("【服务进程】等待响应异常，信息为：%s" % e)
			self.logger.info("【服务进程】-------------------------浮屠长生 响应结果结束-------------------------")
		except Exception as e:
			self.logger.error("【服务进程】创建服务进程异常，异常信息为：%s" % traceback.format_exc())
		finally:
			"""判断是否为空"""
			if manager:
				manager.queue_close()




	def kafka_queue_manager_helper(self, server_dict):
		"""
		生产
		:param server_dict:
		:return:
		"""
		product = None
		try:
			product = KafkaProducerHelper()
			"""添加任务"""
			for key, value in server_dict.items():
				if not value:
					continue
				"""生产数据"""
				[product.send_json_msg(item, key) for item in value]
		except Exception as e:
			self.logger.error("【服务进程】创建服务进程异常，异常信息为：%s" % traceback.format_exc())
		finally:
			"""判断是否为空"""
			if product:
				product.close()



	def redis_queue_manager_helper(self, server_dict):
		"""
		生产
		:param server_dict:
		:return:
		"""
		try:
			redis_helper = RedisHelper()
			"""添加任务"""
			for key, value in server_dict.items():
				if not value:
					continue
				"""生产数据"""
				[redis_helper.lpush_item(item, key) for item in value]
		except Exception as e:
			self.logger.error("【服务进程】创建服务进程异常，异常信息为：%s" % traceback.format_exc())



	def deal_with_result_data(self, task_dict):
		"""
		按服务器IP注册队列
		:param task_dict:
		:return:
		"""
		"""获取休眠时间"""
		account_sleep_time = BusiBaseConfService().search_key_return_value((busi_config.ACCOUNT_SLEEP_TIME))
		sleep_time = account_sleep_time.split("|")
		time_out = random.randint(int(sleep_time[0]), int(sleep_time[1]))
		while task_dict:
			"""按服务器生成队列"""
			server_dict = {}
			queue_length = 0
			for key in list(task_dict.keys()):
				"""判断是否为空"""
				if not task_dict[key]:
					del task_dict[key]
					continue
				"""取值"""
				item = task_dict[key].pop()
				queue_length += 1
				server_ip_name = "get_%s_queue" % item.get("serverIp").replace(".", "_")
				if server_ip_name in task_dict:
					server_dict[server_ip_name].append(item)
				else:
					server_dict.setdefault(server_ip_name, [])
					server_dict[server_ip_name].append(item)
			"""判空"""
			if task_dict:
				self.redis_queue_manager_helper(server_dict)
				self.logger.info("账号休眠，休眠时长：%s秒" % time_out)
				time.sleep(time_out)


	def task_thread_submit(self, item, redis_key, task_dict):
		"""
		多线程处理数据，并对结果以邮箱名称分组
		:param item:
		:param redis_key:
		:param task_dict:
		:return:
		"""
		try:
			if type(item) == str:
				item = json.loads(item)
			result_item = self.observer(item)
			"""设置redis key值"""
			result_item["redis_key"] = redis_key
			user_name = result_item.get("userName")
			"""按邮箱名分组"""
			if user_name in task_dict:
				task_dict[user_name].append(result_item)
			else:
				task_dict.setdefault(user_name, [])
				task_dict[user_name].append(result_item)
		except BusinessExcetion as e:
			self.logger.error("【服务进程】处理队列异常，触发回滚，异常信息为：%s" % e)
			RedisHelper().lpush_item(item, redis_key)
		except Exception as e:
			self.logger.error("【服务进程】读取任务队列异常，信息为：%s" % traceback.format_exc())


	def processing_task(self, key, queue_length):
		"""
		按任务优先级处理数据
		:param key: 任务队列key值
		:param queue_length: 当前队列长度
		:return:
		"""
		"""读取最大量"""
		max_redis_read_length = BusiBaseConfService().search_key_return_value((busi_config.MAX_REDIS_READ_LENGTH))
		self.logger.info("单次最大处理量为：%s" % max_redis_read_length)
		"""读取redis列表"""
		result = BusinessUtil.get_redis_lpop_by_key_and_length(key, queue_length, int(max_redis_read_length))
		"""判空"""
		if not result:
			return
		"""最大线程数"""
		thread_max_workers = BusiBaseConfService().search_key_return_value((busi_config.THREAD_MAX_WORKERS))
		"""按发送邮箱名称分组"""
		task_dict = {}
		with ThreadPoolExecutor(max_workers=int(thread_max_workers)) as executor:
			future_list = []
			"""循环"""
			for item in result:
				if item:
					future = executor.submit(self.task_thread_submit, item, key, task_dict)
					future_list.append(future)
			"""等待子线程结束"""
			wait(future_list, timeout=10)
		"""处理队列数据"""
		self.deal_with_result_data(task_dict)

	def sort_key(key):
		taskCode, server_index, name, index = key.split("_")
		return index


	def instance(self):
		"""
		调度处理任务队列数据
		:return:
		"""
		try:
			"""获取休眠时间"""
			product_sleep_time = BusiBaseConfService().search_key_return_value((busi_config.PRODUCT_SLEEP_TIME))
			sleep_time = product_sleep_time.split("|")
			time_out = random.randint(int(sleep_time[0]), int(sleep_time[1]))
			"""判断是否存在发送中的任务 不存在 则直接返回"""
			if not self.search_task_code_by_server_ip():
				self.logger.info("【服务进程】不存在发送中的任务，日常生成休眠，休眠时长：%s分" % time_out)
				time.sleep(time_out * 60)
				return
			"""读取任务队列"""
			task_name_list = self.get_task_list()
			if not task_name_list:
				self.logger.info("【服务进程】任务列表为空，日常生成休眠，休眠时长：%s分" % time_out)
				time.sleep(time_out*60)
				return
			"""判断账号"""
			if not self.check_valid_account():
				self.logger.info("【服务进程】无有效账号，日常生成休眠，休眠时长：%s分" % time_out)
				time.sleep(time_out * 60)
				return
			"""任务列表排序"""
			def sort_key(key):
				taskCode, server_index, name, index = key.split("_")
				return index
			task_name_list.sort(key=sort_key)
			self.logger.info("【服务进程】任务列表为：%s" % task_name_list)
			"""按任务优先级读取"""
			for task in task_name_list:
				queue_length = BusinessUtil.get_redis_llen_by_key(task)
				"""队列为空"""
				if not queue_length or queue_length == 0:
					continue
				"""出队列"""
				self.processing_task(task, queue_length)
				break
		except Exception as e:
			self.logger.error("【服务进程】服务进程异常，异常信息为：%s" % traceback.format_exc())


	def check_valid_account(self):
		"""
		校验有效邮箱
		:return:
		"""
		account_list = SendEmailAccountService().search_valid_account(self.public_ip)
		if account_list:
			return True
		# """查询未使用的账号"""
		# flag = SendEmailAccountService().search_has_valid_account(self.public_ip)
		# if flag:
		# 	self.logger.info("【校验有效邮箱】查询是否含有未使用的账号")
		# 	return True
		"""获取账号重开间隔时间"""
		account_reopen_time = BusiBaseConfService().search_key_return_value((busi_config.ACCOUNT_REOPEN_TIME))
		"""查询触发频率过快的账号剩余量， 如还有剩余，尝试重新激活"""
		return SendEmailAccountService().search_lock_account(int(account_reopen_time))



	def search_task_code_by_server_ip(self):
		"""
		通过ip查询当前任务编号
		:return: taskCode
		"""
		result = TaskService().search_task_code_by_server_ip(self.public_ip)
		if not result:
			return False
		"""设置任务编号"""
		self.task_code = result.get("taskCode", "")
		self.relId = result.get("relId")
		return True


	def get_send_min_max_time(self):
		"""
		获取发送时间段
		:return:
		"""
		send_min_max_time = BusiBaseConfService().search_key_return_value((busi_config.SEND_MIN_MAX_TIME), "9|20")
		"""数据分割"""
		min_time, max_time = send_min_max_time.split("|")

		return [min_time, max_time]


	def get_batch_sleep_time(self):
		"""
		获取休眠时间
		:return:
		"""
		batch_sleep_time = BusiBaseConfService().search_key_return_value((busi_config.BUSI_BATCH_SLEEP_TIME), "5|8")
		min_time, max_time = batch_sleep_time.split("|")
		"""休眠时长"""
		time_out = random.randint(int(min_time), int(max_time))
		return time_out



	def task_product_time(self):
		"""
		服务进程 定时启动服务进程
		:return:
		"""
		while True:
			self.logger.info("=============================浮屠长生 启动生产进程=============================")
			"""获取发送时间段"""
			send_time = self.get_send_min_max_time()
			"""获取当前时间"""
			hour = int(time.strftime('%H', time.localtime(time.time())))
			time_out = self.get_batch_sleep_time()
			if hour > int(send_time[1]) or hour < int(send_time[0]):
				self.logger.info("当前时间未在发送时间段内容，进行休眠，休眠时长[%s]分钟" % time_out)
				time.sleep(60 * time_out)
				continue
			self.instance()
			self.logger.info("=============================浮屠长生 生产进程关闭=============================")





if __name__ == "__main__":
	"""定时启动"""
	TaskProduct().task_product_time()








