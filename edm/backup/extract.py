#!/usr/bin/python3
# -*- coding: utf-8 -*-
import traceback
import random
import time
from config import busi_config
from base.user_logger import UserLogger
from util.business_util import BusinessUtil
from service.primary_data_service import PrimaryDataService
from service.busi_base_conf_service import BusiBaseConfService
from service.marketing_data_service import MarketingDataService
from observer.subject_data import SubjectData
from observer.marketing_observer import MarketingObserver
from observer.task_observer import TaskObserver
from observer.check_black_observer import CheckBlackObserver
from observer.check_smtp_observer import CheckSmtpObserver
from service.send_email_account_service import SendEmailAccountService
from service.task_service import TaskService
from service.file_read_record_service import FileReadRecordService
from base import global_argument
from collect import Collect
from util.file_helper import FileHelper
import os



def sort_key(key):
	"""排序规则"""
	name, index = key.split("_")
	return int(index.split(".")[0])


class Extract(object):
	"""
	提取营销数据（提取用户数据并添加到任务列表）
	"""
	def __init__(self):
		"""
		初始日志
		"""
		self.logger = UserLogger.getlog()
		"""当前服务器IP地址"""
		self.public_ip = BusinessUtil.get_public_ip()
		"""设置全局变量"""
		global_argument.set_value(self.public_ip)
		self.task_code = None
		self.relId = None
		self.task_type = None


	def get_file_name_list_base_path(self):
		"""
		通过基础路径获取文件列表
		:return:
		"""
		task_file_base_path = busi_config.TASK_BASE_PATH % self.task_code
		"""获取文件列表"""
		file_name_list = os.listdir(task_file_base_path)
		"""排序"""
		file_name_list.sort(key=sort_key)
		self.logger.info("【读取文件列表】文件排序结果为：%s" % file_name_list)
		return file_name_list


	def get_file_name(self):
		"""
		获取当前文件名
		:return:
		"""
		"""通过任务号查询是否存在发送中的数据记录"""
		file_result = FileReadRecordService().search((self.task_code, 0))
		if file_result:
			"""查到结果"""
			return file_result[0]
		"""获取文件名"""
		file_name_list = self.get_file_name_list_base_path()
		"""不存在文件列表"""
		if not file_name_list:
			return False
		"""查询读取完成的记录"""
		file_result = FileReadRecordService().search((self.task_code, 1))
		"""如果未查到记录 说明该任务是首次执行 返回第一个文件"""
		if not file_result:
			return {"taskCode": self.task_code, "fileName": file_name_list[0], "readOffset": 0, "is_new": True}
		"""如果查询到记录 剔除当前已存在的记录 并返回新文件名称"""
		table_file_name_list = list()
		[table_file_name_list.append(item.get("fileName")) for item in file_result]
		"""取两个list差集"""
		file_list = list(set(file_name_list) ^ set(table_file_name_list))
		"""排序 取第一个"""
		file_list.sort(key=sort_key)
		self.logger.info("【差集结果排序】排序结果为：%s" % file_list)
		if not file_list:
			return False
		return {"taskCode": self.task_code, "fileName": file_list[0], "readOffset": 0, "is_new": True}


	def search_result_by_file(self, batchCode, batch_max_length):
		"""
		读取文件内容
		:param batchCode:
		:param batch_max_length:
		:return:
		"""
		"""获取文件名"""
		file_result = self.get_file_name()
		if not file_result:
			return False
		"""获取文件路径"""
		base_path = busi_config.TASK_BASE_PATH % self.task_code
		file_path = "%s%s" % (base_path, file_result.get("fileName"))
		"""读取文件内容"""
		read_result = FileHelper.read_seek(file_path, int(file_result.get("readOffset")), int(batch_max_length))
		"""判断结果"""
		if not read_result:
			return False
		"""偏移量"""
		offset = read_result.get("offset", 0)
		"""文件大小"""
		file_size = read_result.get("file_size", 0)
		"""读取内容"""
		context_list = read_result.get("result", [])
		"""更新读取内容"""
		result = list()
		[result.append({"email": "", "mobile": item, "batchCode": batchCode, "originalBatchCode": self.task_code}) for item in context_list]
		"""读取文件内容列表长度"""
		read_lines_size = len(result)
		"""记录状态"""
		status = 1 if offset == file_size else 0
		"""入库更新操作"""
		is_new = file_result.get("is_new", False)
		if is_new:
			"""插入记录表"""
			flag = FileReadRecordService().insert((self.task_code, file_result.get("fileName"), offset, read_lines_size, status))
		else:
			"""更新记录表"""
			flag = FileReadRecordService().update((offset, read_lines_size, status, self.task_code, file_result.get("fileName")))
		"""更新记录失败"""
		if not flag:
			return False
		return result



	def get_primamary_list(self, batchCode):
		"""
		获取营销数据
		:return:
		"""
		if not self.task_code:
			self.logger.info("【提取数据】不存在发送中的任务，流程结束")
			return False
		"""拉取单批次发送量"""
		batchMaxLength = BusiBaseConfService().search_key_return_value((busi_config.BATCH_MAX_LENGTH), "3")
		primaryDataService = PrimaryDataService()
		"""获取允许重发的ip"""
		allow_resend_server_ip = BusiBaseConfService().search_key_return_value((busi_config.ALLOW_RESEND_SERVER_IP))
		"""判断是否为主程序"""
		if allow_resend_server_ip != self.public_ip:
			return False
		"""判断类型"""
		if str(self.task_type) == "1":
			"""更新数据"""
			primaryDataService.update((batchCode, self.task_code, int(batchMaxLength)))
			"""查询数据"""
			result = primaryDataService.search((batchCode))
		else:
			"""文件中读取"""
			result = self.search_result_by_file(batchCode, int(batchMaxLength))
		return result




	def observer(self, result):
		"""
		数据处理（营销数据入库、队列检查、任务队列）
		:return:
		"""
		if not result:
			self.logger.info("【提取数据】提取数据为空，流程结束")
			return
		subject = SubjectData()
		"""1、检查队列 黑名单"""
		observer1 = CheckBlackObserver(subject)
		"""2、检查队列 smtp"""
		observer2 = CheckSmtpObserver(subject)
		"""3、营销数据入库"""
		observer3 = MarketingObserver(subject)
		"""4、PUSH任务队列"""
		observer4 = TaskObserver(subject)
		subject.attach(observer1)
		subject.attach(observer2)
		subject.attach(observer3)
		subject.attach(observer4)
		subject.email_list = result
		subject.rel_id = self.relId
		subject.notify()



	def roll_back(self, batchCode):
		"""
		回退记录
		:param batchCode:
		:return:
		"""
		PrimaryDataService().update_roll_back((batchCode, self.task_code))



	def resend_instance(self):
		"""
		邮件重发
		:return:
		"""
		self.logger.info("---------------------------------浮屠长生 开始提取重发数据---------------------------------")
		try:
			"""查询配置文件 最大重发量"""
			reSendMaxLength = BusiBaseConfService().search_key_return_value((busi_config.RE_SEND_MAX_LENGTH), "5")
			result = MarketingDataService().resend_search((self.task_code, reSendMaxLength))
			"""数据处理"""
			self.observer(result)
		except Exception as e:
			self.logger.error("【数据提取】提取重发数据异常，异常信息为：%s" % traceback.format_exc())
		self.logger.info("---------------------------------浮屠长生 提取重发数据结束---------------------------------")



	def instance(self):
		"""
		:return:
		"""
		self.logger.info("---------------------------------浮屠长生 开始提取数据---------------------------------")
		batch_code = None
		try:
			"""生成主批次号"""
			batch_code = BusinessUtil.get_uniqu_time()
			self.logger.info("【提取数据】生成当前主批次号为：%s" % batch_code)
			"""提取数据"""
			result = self.get_primamary_list(batch_code)
			"""获取待发送邮箱，并集"""
			marketing_email = BusiBaseConfService().search_key_return_value((busi_config.MARKETING_EMAIL_KEY), "139.com")
			result = BusinessUtil.convert_data(result, marketing_email, False)
			"""数据处理"""
			self.observer(result)
		except Exception as e:
			self.logger.error("【数据提取】数据提取异常，回滚批次为：%s，异常信息为：%s" % (batch_code, traceback.format_exc()))
			self.roll_back(batch_code)
		self.logger.info("---------------------------------浮屠长生 提取数据结束---------------------------------")


	def get_task_list(self):
		"""
		获取任务列表
		:return:
		"""
		pattern = "%s_%s_pagoda_[0-9]*" % (self.task_code, self.relId)
		result = BusinessUtil.get_redis_name_by_keys(pattern)
		self.logger.info("【数据提取】读取到的任务列表为：%s" % result)
		return result


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
		self.task_type = result.get("taskType", "")
		return True


	def task_extract_time(self):
		"""
		定时任务
		:return:
		"""
		send_count = 0
		send_report = 0
		while True:
			self.logger.info("=============================浮屠长生 开始第[%s]定时任务==================================" % send_count)
			"""获取发送时间段"""
			send_min_max_time = BusiBaseConfService().search_key_return_value((busi_config.SEND_MIN_MAX_TIME), "9|20")
			"""数据分割"""
			send_time = send_min_max_time.split("|")
			"""获取休眠时间"""
			batch_sleep_time = BusiBaseConfService().search_key_return_value((busi_config.BUSI_BATCH_SLEEP_TIME), "5|8")
			sleep_time = batch_sleep_time.split("|")
			"""获取允许重发的ip"""
			allow_resend_server_ip = BusiBaseConfService().search_key_return_value((busi_config.ALLOW_RESEND_SERVER_IP))

			"""休眠时长"""
			time_out = random.randint(int(sleep_time[0]), int(sleep_time[1]))
			"""获取当前时间"""
			hour = int(time.strftime('%H', time.localtime(time.time())))
			if hour > int(send_time[1]):
				self.logger.info("当前时间未在发送时间段内容，进行休眠，休眠时长[%s]分钟" % time_out)
				time.sleep(60 * time_out)
			elif hour < int(send_time[0]):
				"""判断是否在发送时间段内，如果不存在的话跳过 0~9"""
				"""若标志位为0"""
				if send_report == 0 and allow_resend_server_ip == self.public_ip and self.get_task_list():
					send_report = 1
					"""获取账号重开间隔时间"""
					account_reopen_time = BusiBaseConfService().search_key_return_value((busi_config.ACCOUNT_REOPEN_TIME))
					"""更新账号"""
					SendEmailAccountService().search_and_update_account(self.public_ip, account_reopen_time)
				send_count = 0
				self.logger.info("当前时间未在发送时间段内容，进行休眠，休眠时长[%s]分钟" % time_out)
				time.sleep(60 * time_out)
			elif not self.search_task_code_by_server_ip():
				self.logger.info("【提取数据】不存在发送中的任务，流程结束")
				time.sleep(60 * time_out)
			elif send_count != 0 and not self.get_task_list():
				"""如果不是当天第一次发送，且缓存记录为空"""
				"""发送次数"""
				send_count += 1
				send_report = 0
				"""
				收取邮件
				"""
				Collect().instance_server_ip()
				"""
				数据二次营销 大于5次就不再营销
				"""
				if allow_resend_server_ip == self.public_ip:
					self.resend_instance()
				self.instance()
				"""休眠"""
				self.logger.info("当前第[%s]次发送，缓存信息为空，进行休眠，休眠时长[%s]分钟" % (send_count, time_out))
				time.sleep(60 * time_out)
			elif self.get_task_list():
				"""如果缓存记录不为空，则休眠"""
				send_report = 0
				self.logger.info("当前第[%s]次发送，缓存信息不为空，进行休眠，休眠时长[%s]分钟" % (send_count, time_out))
				time.sleep(60 * time_out)
			else:
				"""如果缓存记录为空，进行消费生产"""
				send_count += 1
				send_report = 0
				"""生产"""
				self.instance()
				self.logger.info("当前第[%s]次发送，生成缓存信息，进行休眠，休眠时长[%s]分钟" % (send_count, time_out))
				time.sleep(60*time_out)
			self.logger.info("=============================浮屠长生 结束本次定时任务==================================")



if __name__ == "__main__":
	Extract().task_extract_time()
