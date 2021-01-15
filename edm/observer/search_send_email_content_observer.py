#!/usr/bin/python3
# -*- coding: utf-8 -*-
from exception.business_exception import BusinessExcetion
from base.observer import Observer
from service.template_service import TemplateService
from service.busi_base_conf_service import BusiBaseConfService
from service.used_of_count_service import UsedOfCountService
from config import busi_config
import random
import json
import time


class SearchSendEmailContentObserver(Observer):
	"""
	确认发送内容
	"""
	def update(self):
		"""
		选择发送内容
		:return:
		"""
		self.logger.info("【任务队列】2、筛选发送内容")
		result = self.subject.email_item
		"""当前task_code"""
		task_code = result.get("task_code")
		"""查询发送内容"""
		template_list = TemplateService().search(task_code)
		"""查询筛选规则"""
		resend_rules = BusiBaseConfService().search_key_return_value((busi_config.RESEND_RULES),"1|1|1")
		"""分割规则"""
		resend_rules_list = resend_rules.split("|")
		"""判断是否有发送内容"""
		template_ext_code = result.get("templateExtCode", "")
		if template_ext_code:
			"""发送内容存在，筛选当前发送内容"""
			send_email_content_item = self.select_send_email_content(template_list, template_ext_code)
		else:
			"""待过滤发送内容"""
			filter_template_ext_code = result.get("reSendTemplateExtCode", "")
			if not filter_template_ext_code:
				filter_template_ext_code = ""
			"""筛选发送内容"""
			send_email_content_item = self.filter_send_template_ext_code(template_list, resend_rules_list[2],filter_template_ext_code)
		if not send_email_content_item:
			raise BusinessExcetion("T02", "未查到有效邮件内容，进行回滚")
		self.logger.info("【任务队列】筛选发送内容：%s" % send_email_content_item.get("templateExtCode"))
		result.update(send_email_content_item)





	def filter_send_template_ext_code(self, template_list, resend_reles, filter_template_ext_code=None):
		"""
		过滤发送内容
		:param template_list:
		:param resend_reles:
		:param filter_template_ext_code:
		:return:
		"""
		"""判断类型 如果传入数据为str 转化为列表"""
		if type(template_list) == str:
			template_list = json.loads(template_list)
		queue_list = []
		if resend_reles == "1":
			[queue_list.append(item) for item in template_list if filter_template_ext_code.find(item.get("templateExtCode")) < 0]
		else:
			queue_list = template_list
		if not queue_list:
			self.logger.info("【任务队列】未查到有效邮件内容")
			return False
		"""生成随机数"""
		item = random.choice(queue_list)
		return item


	def select_send_email_content(self, template_list, template_ext_code):
		"""
		筛选发送内容
		:param template_list:
		:param template_ext_code:
		:return:
		"""
		queue_list = []
		if type(template_list) == str:
			template_list = json.loads(template_list)
		[queue_list.append(item) for item in template_list if template_ext_code == item.get("templateExtCode")]
		if not queue_list:
			self.logger.info("【任务队列】未查到有效邮件内容")
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


if __name__ == "__main__":
	pass





