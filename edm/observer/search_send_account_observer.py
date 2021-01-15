#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from service.busi_base_conf_service import BusiBaseConfService
from service.used_of_count_service import UsedOfCountService
from service.send_email_account_service import SendEmailAccountService
from exception.business_exception import BusinessExcetion
from config import busi_config
import random
import time
import json


class SearchSendAccountObserver(Observer):
	"""
	筛选发送账号
	"""
	def update(self):
		"""
		筛选发送账号
		:return:
		"""
		self.logger.info("【任务队列】1、筛选发送账号")
		result = self.subject.email_item
		"""当前IP"""
		public_ip = result.get("public_ip")
		account_list = SendEmailAccountService().search_valid_account(public_ip)
		if not account_list:
			self.logger.info("【发送邮件】开始变更账号信息")
			account_reopen_time = BusiBaseConfService().search_key_return_value((busi_config.ACCOUNT_REOPEN_TIME))
			SendEmailAccountService().search_and_update_account(public_ip, int(account_reopen_time))
			raise BusinessExcetion("T02", "未查询到有效账号")
		"""查询筛选规则"""
		resend_rules = BusiBaseConfService().search_key_return_value((busi_config.RESEND_RULES),"1|1|1")
		"""分割规则"""
		resend_rules_list = resend_rules.split("|")
		"""判断是否有发送账号"""
		send_account = result.get("sendAccount", "")
		if send_account:
			"""发送账号存在，筛选当前账号信息"""
			send_account_item = self.select_send_account(account_list, send_account)
		else:
			"""待过滤发送账号"""
			filter_send_account = result.get("reSendAccount", "")
			if not filter_send_account:
				filter_send_account = ""
			"""筛选发送账号"""
			send_account_item = self.filter_send_account(account_list, resend_rules_list[1], filter_send_account)
		if not send_account_item:
			raise BusinessExcetion("T02", "未查到有效账号，进行回滚")
		self.logger.info("【任务队列】筛选发送账号：%s" % send_account_item.get("userName"))
		result.update(send_account_item)
		self.set_used_of_count_record(send_account_item.get("userName"), 2)



	def filter_send_account(self, account_list, resend_reles, filter_send_account=None):
		"""
		过滤发送账号
		:param account_list:
		:param resend_reles:
		:param filter_send_account:
		:return:
		"""
		if type(account_list) == str:
			account_list = json.loads(account_list)
		queue_list = []
		if resend_reles == "1":
			[queue_list.append(item) for item in account_list if filter_send_account.find(item.get("userName")) < 0]
		else:
			queue_list = account_list
		if not queue_list:
			self.logger.info("【提取账号】未查到有效发送账号")
			return False
		"""生成随机数"""
		item = random.choice(queue_list)
		return item


	def select_send_account(self, account_list, send_account):
		"""
		筛选发送账号
		:param account_list:
		:param send_account:
		:return:
		"""
		if type(account_list) == str:
			account_list = json.loads(account_list)
		queue_list = []
		[queue_list.append(item) for item in account_list if send_account == item.get("userName")]
		if not queue_list:
			self.logger.info("【提取账号】未查到有效发送账号")
			return False
		return queue_list[0]



	def set_used_of_count_record(self, used_of_content, used_type=1):
		"""
		添加账号使用量记录
		:param used_of_content:
		:param used_type:
		:return:
		"""
		timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
		start = "%s 00:00:00" % timeStr
		end = "%s 23:59:59" % timeStr
		param = {
			"start": start,
			"end": end,
			"usedOfContent": used_of_content,
			"usedType": used_type
		}
		UsedOfCountService().insert_update(param)





