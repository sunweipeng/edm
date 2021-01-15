#!/usr/bin/python3
# -*- coding: utf-8 -*-
import traceback
import time
from base.user_logger import UserLogger
from observer.subject_collect import SubjectCollect
from service.used_of_count_service import UsedOfCountService
from service.send_email_account_service import SendEmailAccountService
from observer.pop3_collect_observer import POP3CollectObserver
from observer.parse_email_observer import ParseEmailObserver
from observer.pop3_record_observer import POP3RecordObserver
from observer.update_marketing_observer import UpdateMarketingObserver
from service.busi_base_conf_service import BusiBaseConfService
from config import busi_config
from base import global_argument
from util.business_util import BusinessUtil



class Collect(object):
	"""
	收取邮件
	"""
	def __init__(self):
		"""
		初始化
		"""
		self.logger = UserLogger.getlog()
		"""当前服务器IP地址"""
		self.public_ip = BusinessUtil.get_public_ip()
		"""设置全局变量"""
		global_argument.set_value(self.public_ip)


	def get_send_email_account_list(self):
		"""
		获取当天邮件发送账号
		:return:
		"""
		timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
		start = "%s 00:00:00" % timeStr
		end = "%s 23:59:59" % timeStr
		result = UsedOfCountService().search_by_type((start, end))
		if not result:
			"""查询全部账号"""
			result = SendEmailAccountService().search_pop()
		return result



	def get_send_email_account_list_by_server_ip(self):
		"""
		通过ip查询账号
		:return:
		"""
		result = SendEmailAccountService().search_pop_server_ip(self.public_ip)
		return result


	def observer(self, result):
		"""
		观察者
		:return:
		"""
		subject = SubjectCollect()
		"""1、收取邮件"""
		observer1 = POP3CollectObserver(subject)
		"""2、解析邮件内容"""
		observer2 = ParseEmailObserver(subject)
		"""3、收取记录入库"""
		observer3 = POP3RecordObserver(subject)
		"""4、更新营销数据"""
		observer4 = UpdateMarketingObserver(subject)
		subject.attach(observer1)
		subject.attach(observer2)
		subject.attach(observer3)
		subject.attach(observer4)
		subject.pop3_account = result
		subject.notify()

	def instance(self):
		"""
		收取邮件
		:return:
		"""
		self.logger.info("=============================浮屠长生 开始收取邮件=============================")
		"""获取发送账号"""
		result = self.get_send_email_account_list()
		if not result:
			"""未查到发送账号"""
			self.logger.info("=============================浮屠长生 收取邮件结束=============================")
			return
		"""账号间隔休眠时长"""
		collect_account_sleep_time = BusiBaseConfService().search_key_return_value((busi_config.COLLECT_ACCOUNT_SLEEP_TIME), "0")
		self.logger.info("账号间隔休眠时长[%s]秒" % collect_account_sleep_time)
		for item in result:
			try:
				self.observer(item)
				time.sleep(float(collect_account_sleep_time))
			except Exception as e:
				self.logger.error("【收取邮件】收取邮件异常，异常信息为：%s" % traceback.format_exc())
		self.logger.error("=============================浮屠长生 收取邮件结束=============================")



	def instance_server_ip(self):
		"""
		收取邮件（通过服务ip）
		:return:
		"""
		self.logger.info("=============================浮屠长生 开始收取邮件=============================")
		"""获取发送账号"""
		result = self.get_send_email_account_list_by_server_ip()
		if not result:
			"""未查到发送账号"""
			self.logger.info("=============================浮屠长生 收取邮件结束=============================")
			return
		"""账号间隔休眠时长"""
		collect_account_sleep_time = BusiBaseConfService().search_key_return_value((busi_config.COLLECT_ACCOUNT_SLEEP_TIME), "0")
		self.logger.info("账号间隔休眠时长[%s]秒" % collect_account_sleep_time)

		for item in result:
			try:
				self.observer(item)
				time.sleep(float(collect_account_sleep_time))
			except Exception as e:
				self.logger.error("【收取邮件】收取邮件异常，异常信息为：%s" % traceback.format_exc())
		self.logger.error("=============================浮屠长生 收取邮件结束=============================")


	def task_collect_time(self):
		"""
		收取邮件
		:return:
		"""
		while True:
			"""开始收取邮件"""
			self.instance()
			"""休眠"""
			collect_sleep_time = BusiBaseConfService().search_key_return_value((busi_config.COLLECT_SLEEP_TIME), "15")
			self.logger.info("收取邮件完成，进行休眠，休眠时长[%s]分钟" % collect_sleep_time)
			time.sleep(60 * int(collect_sleep_time))



if __name__ == "__main__":
	Collect().task_collect_time()
