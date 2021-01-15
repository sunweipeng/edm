#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from base.observer import Observer
from service.server_conf_service import ServerConfService
from service.busi_base_conf_service import BusiBaseConfService
from service.used_of_count_service import UsedOfCountService
from config import busi_config
from exception.business_exception import BusinessExcetion
import random
import json


class SearchServerIpObserver(Observer):
	"""
	筛选发送服务器
	"""
	def update(self):
		"""
		筛选发送服务器
		:return:
		"""
		self.logger.info("【数据提取】3、筛选服务器")
		result = self.subject.email_item
		"""查询服务器数据"""
		server_list = ServerConfService().search()
		"""查询筛选规则"""
		resend_rules = BusiBaseConfService().search_key_return_value((busi_config.RESEND_RULES),"1|1|1")
		"""分割规则"""
		resend_rules_list = resend_rules.split("|")
		"""判断是否有服务器IP"""
		server_ip = result.get("serverIp", "")
		if server_ip:
			"""服务器IP存在，筛选当前服务器信息"""
			server_item = self.select_server_ip(server_list, server_ip)
		else:
			"""待过滤服务器ip"""
			filter_ip = result.get("reSendServerIp", "")
			"""筛选服务器"""
			if not filter_ip:
				filter_ip = ""
			server_item = self.filter_server_ip(server_list, resend_rules_list[0], filter_ip)
		if not server_item:
			raise BusinessExcetion("T04", "未查到有效的服务器地址")
		self.logger.info("【任务队列】筛选服务器IP：%s" % server_item.get("serverIp"))
		result.update(server_item)
		"""更新/添加使用量"""
		#self.set_used_of_count_record(server_item.get("serverIp"))



	def filter_server_ip(self, server_list, resend_reles, filter_ip=None):
		"""
		过滤服务器
		:param server_list:
		:param resend_reles:
		:param filter_ip:
		:return:
		"""
		if type(server_list) == str:
			server_list = json.loads(server_list)
		queue_list = []
		if resend_reles == "1":
			[queue_list.append(item) for item in server_list if filter_ip.find(item.get("serverIp")) < 0]
		else:
			queue_list = server_list
		if not queue_list:
			self.logger.info("【数据提取】未查到有效服务器，进行随机抽取")
			item = random.choice(server_list)
			return item
		"""生成随机数"""
		item = random.choice(queue_list)
		return item


	def select_server_ip(self, server_list, server_ip):
		"""
		筛选服务器
		:param server_list:
		:param server_ip:
		:return:
		"""
		if type(server_list) == str:
			server_list = json.loads(server_list)
		queue_list = []
		[queue_list.append(item) for item in server_list if server_ip == item.get("serverIp")]
		if not queue_list:
			self.logger.info("【数据提取】未查到有效服务器，进行随机抽取")
			item = random.choice(server_list)
			return item
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






