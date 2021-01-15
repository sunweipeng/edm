#!/usr/bin/python3
# -*- coding: utf-8 -*-
import traceback
import time
import json
import random
from base.user_logger import UserLogger
from util.business_util import BusinessUtil
from observer.consume_subject import ConsumeSubject
from observer.smtp_send_observer import SMTPSendObserver
from observer.send_record_observer import SendRecordObserver
from observer.used_of_count_observer import UsedOfCountObserver
from observer.check_return_code_observer import CheckReturnCodeObserver
from observer.send_email_update_marketing_data_observer import SendEmailUpdateMarketingDataObserver
from observer.speed_limit_check_observer import SpeedLimitCheckObserver
from observer.send_email_account_check_observer import SendEmailAccountCheckObserver
from exception.business_exception import BusinessExcetion
from concurrent.futures import ThreadPoolExecutor, wait
from config import busi_config
from util.redis_helper import RedisHelper
from service.busi_base_conf_service import BusiBaseConfService
from util.kafka_helper import KafkaConsumerHelper
from util.queue_manager_helper import QueueManagerHelper
from multiprocessing.managers import RemoteError
from base import global_argument
import copy





class TaskConsume(object):
	"""
	分布式任务进程
	"""
	def __init__(self):
		self.logger = UserLogger.getlog()
		"""当前服务器IP地址"""
		self.public_ip = BusinessUtil.get_public_ip()
		"""设置全局变量"""
		global_argument.set_value(self.public_ip)
		"""选择消费机制"""
		self.task_choice_pattern = self.public_ip



	def observer(self, result):
		"""
		观察者 发送邮件并入库
		:param result:
		:return:
		"""
		subject = ConsumeSubject()
		"""0、账号状态检查"""
		observer0 = SendEmailAccountCheckObserver(subject)
		"""1、限速检查"""
		observer1 = SpeedLimitCheckObserver(subject)
		"""2、发送邮件"""
		observer2 = SMTPSendObserver(subject)
		"""3、返回码检查"""
		observer3 = CheckReturnCodeObserver(subject)
		"""4、记录内容"""
		observer4 = SendRecordObserver(subject)
		"""5、更新营销数据"""
		observer5 = SendEmailUpdateMarketingDataObserver(subject)
		"""6、账号使用量"""
		observer6 = UsedOfCountObserver(subject)
		subject.attach(observer0)
		subject.attach(observer1)
		subject.attach(observer2)
		subject.attach(observer3)
		subject.attach(observer4)
		subject.attach(observer5)
		subject.attach(observer6)
		subject.email_item = result
		subject.notify()
		return subject.email_item


	def get_task_list(self):
		"""
		服务进程注册队列名称
		:return:
		"""
		register_list = list()
		register_list.append("get_result_queue")
		register_list.append("get_%s_queue" % self.task_choice_pattern.replace(".", "_"))
		return register_list



	def task_thread_submit(self, task_queue_item):
		"""
		多线程发送邮件
		:param task_queue_item:
		:return:
		"""
		retCode = None
		retMsg = None
		"""复制备份"""
		task_item = copy.deepcopy(task_queue_item)
		try:
			"""确定当前服务器"""
			serverIp = task_queue_item.get("serverIp")
			if self.public_ip != serverIp:
				task_queue_item["serverIp"] = self.public_ip
			self.logger.info("【消费】读取到的队列项信息为：%s" % task_queue_item)
			"""获取返回码"""
			result_item = self.observer(task_queue_item)
			retCode = result_item.get("send_status", "1")
		except BusinessExcetion as e:
			self.logger.error("【消费】读取任务队列异常，开始信息回滚，信息为：%s" % e)
			retCode = e.retCode
			retMsg = e.retMsg
			RedisHelper().lpush_item(task_item, task_item.get("redis_key"))
		except Exception as e:
			self.logger.error("【消费】读取任务队列异常，信息为：%s" % traceback.format_exc())
			retCode = "9999"
			retMsg = "其他异常"
		finally:
			result = {"retCode": retCode, "retMsg": retMsg, "send_server": self.public_ip}
			self.logger.info("【消费】多线程发送邮件结果为：%s" % result)




	def kafka_processing_task(self, message):
		"""
		处理消费队列
		:param message:
		:return:
		"""
		"""最大线程数"""
		thread_max_workers = BusiBaseConfService().search_key_return_value((busi_config.THREAD_MAX_WORKERS))
		"""线程数"""
		with ThreadPoolExecutor(max_workers=int(thread_max_workers)) as executor:
			future_list = []
			"""读取任务队列数据"""
			for msg in message:
				if msg.value:
					item = json.loads(msg.value)
					future = executor.submit(self.task_thread_submit, item)
					future_list.append(future)
			"""等待子线程结束"""
			wait(future_list, timeout=10)


	def manager_processing_task(self, task_queue, result_queue):
		"""
		处理任务队列
		:param task_queue:
		:param result_queue:
		:return:
		"""
		"""最大线程数"""
		thread_max_workers = BusiBaseConfService().search_key_return_value((busi_config.THREAD_MAX_WORKERS))
		"""线程数"""
		with ThreadPoolExecutor(max_workers=int(thread_max_workers)) as executor:
			future_list = []
			"""读取任务队列数据"""
			while not task_queue.empty():
				item = task_queue.get(True, timeout=5)
				self.logger.error("【任务进程】读取队列项数据为：%s" % item)
				future = executor.submit(self.task_thread_submit, item, result_queue)
				future_list.append(future)
			"""等待子线程结束"""
			wait(future_list, timeout=10)


	def processing_task(self, message):
		"""
		处理消费队列
		:param message:
		:return:
		"""
		"""最大线程数"""
		thread_max_workers = BusiBaseConfService().search_key_return_value((busi_config.CONSUME_THREAD_MAX_WORKERS))
		"""线程数"""
		with ThreadPoolExecutor(max_workers=int(thread_max_workers)) as executor:
			future_list = []
			"""读取任务队列数据"""
			for msg in message:
				item = json.loads(msg)
				future = executor.submit(self.task_thread_submit, item)
				future_list.append(future)
			future_list.append(future)
			"""等待子线程结束"""
			wait(future_list, timeout=10)



	def kafka_instance(self):
		"""
		启动kafka消费
		:return:
		"""
		try:
			"""获取订阅信息"""
			kafka_topic = "get_%s_queue" % self.task_choice_pattern.replace(".", "_")
			"""消费者"""
			consumer_helper = KafkaConsumerHelper(kafka_topic)
			consumer = consumer_helper.consumer()
			"""处理消息"""
			self.processing_task(consumer)
			"""处理结束"""
			self.logger.info("【消费】处理结束")
		except Exception as e:
			self.logger.error("【消费】启动消费异常，信息为：%s" % traceback.format_exc())


	def redis_instance(self):
		"""
		启动redis消费
		:return:
		"""
		try:
			"""获取订阅信息"""
			kafka_topic = "get_%s_queue" % self.task_choice_pattern.replace(".", "_")
			"""读取当前redis内数据长度"""
			queue_length = BusinessUtil.get_redis_llen_by_key(kafka_topic)
			"""读取最大量"""
			consume_max_redis_read_length = BusiBaseConfService().search_key_return_value((busi_config.CONSUME_MAX_REDIS_READ_LENGTH))
			self.logger.info("单次最大处理量为：%s" % consume_max_redis_read_length)
			"""读取redis列表"""
			result = BusinessUtil.get_redis_lpop_by_key_and_length(kafka_topic, queue_length, int(consume_max_redis_read_length))
			"""判空"""
			if not result:
				self.logger.info("【消费】未读取到有效数据，流程结束")
				return
			"""处理消息"""
			self.processing_task(result)
			"""处理结束"""
			self.logger.info("【消费】处理结束")
		except Exception as e:
			self.logger.error("【消费】启动消费异常，信息为：%s" % traceback.format_exc())


	def manager_instance(self):
		"""
		启动任务进程
		:return:
		"""
		try:
			self.logger.info("启动子线程")
			"""获取服务进程注册名"""
			task_queue_list = self.get_task_list()
			"""初始化任务进程"""
			manager = QueueManagerHelper(busi_config.QUEUE_MANAGER_ADDRESS, busi_config.QUEUE_MANAGER_AUTH_KEY, task_queue_list, False)
			"""启动任务进程"""
			manager.worker_start()
			"""结果队列"""
			result_queue = manager.server.get_result_queue()
			"""读取任务队列"""
			for item in task_queue_list:
				if item == "get_result_queue":
					continue
				task_queue = eval("manager.server.%s" % item)()
				self.processing_task(task_queue, result_queue)
			"""处理结束"""
			self.logger.info("【任务进程】处理结束")
		except ConnectionRefusedError:
			self.logger.error("【任务进程】请开启服务进程")
		except RemoteError:
			self.logger.error("【任务进程】请开启服务进程")
		except ConnectionResetError:
			self.logger.error("【任务进程】服务端重置链接")
		except BrokenPipeError:
			self.logger.error("【任务进程】服务端关闭链接")
		except EOFError:
			self.logger.error("【任务进程】请开启服务进程")
		except TimeoutError:
			self.logger.error("【任务进程】请开启服务进程")
		except Exception as e:
			self.logger.error("【任务进程】启动任务进程异常，信息为：%s" % traceback.format_exc())


	def get_consume_sleep_time(self):
		consume_sleep_time = BusiBaseConfService().search_key_return_value((busi_config.CONSUME_SLEEP_TIME))
		sleep_time = consume_sleep_time.split("|")
		time_out = random.randint(int(sleep_time[0]), int(sleep_time[1]))
		return time_out


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



	def task_consume_time(self):
		"""
		任务进程，定时监听服务进程队列 间隔时长1秒
		:return:
		"""
		while True:
			"""获取发送时间段"""
			send_time = self.get_send_min_max_time()
			"""获取当前时间"""
			hour = int(time.strftime('%H', time.localtime(time.time())))
			time_out = self.get_batch_sleep_time()
			if hour > int(send_time[1]) or hour < int(send_time[0]):
				self.logger.info("当前时间未在发送时间段内容，进行休眠，休眠时长[%s]分钟" % time_out)
				time.sleep(60 * time_out)
				continue
			self.logger.info("=============================浮屠长生 开始发送邮件=============================")
			with ThreadPoolExecutor(max_workers=1) as executor:
				future_list = []
				future = executor.submit(self.redis_instance)
				future_list.append(future)
				"""等待子进程结束"""
				wait(future_list, timeout=10)
			self.logger.info("子线程结束")
			self.logger.info("=============================浮屠长生 发送邮件结束=============================")
			"""消费休眠时间"""
			time_out = self.get_consume_sleep_time()
			time.sleep(time_out)




if __name__ == "__main__":
	TaskConsume().task_consume_time()



