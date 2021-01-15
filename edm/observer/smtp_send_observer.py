#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import re
from base.observer import Observer
from util.smtp_util import SMTPUtil
from util.business_util import BusinessUtil
from service.proxy_server_conf_service import ProxyServerConfService
from config import busi_config




class SMTPSendObserver(Observer):
	"""
	SMTP发送邮件
	"""
	def update(self):
		"""
		SMTP发送邮件
		:return:
		"""
		self.logger.info("【发送邮件】2、SMTP发送邮件")
		result = self.subject.email_item
		try:
			"""判断服务器是否需要代理"""
			isNeedProxy = result.get("isNeedProxy", 0)
			proxy_server = None
			if isNeedProxy:
				proxy_server = self.select_proxy_server_ip()
			"""初始化SMTP服务器"""
			smtp_server = SMTPUtil(result, proxy_server)
			"""获取发送内容"""
			smtp_msg = self.get_send_msg(smtp_server, result)
			"""smtp发送邮件"""
			smtp_send_result = smtp_server.smtp_send_mail(result.get("userName"), result.get("email"), smtp_msg)
			self.logger.info("【发送邮件】SMTP发送结果：%s" % smtp_send_result)
			"""保存发送结果"""
			result["send_status"] = smtp_send_result.get("retCode")
			result["send_msg"] = smtp_send_result.get("retMsg", "")
		except Exception as e:
			self.logger.error("SMTP发送邮件失败，失败信息为：%s" % e)
			"""投递异常"""
			result["send_status"] = 0
			result["send_msg"] = "投递异常"


	def select_proxy_server_ip(self):
		"""
		选择代理服务器
		:return:
		"""
		"""获取代理服务器"""
		proxy_server_conf = ProxyServerConfService().search((1))
		if not proxy_server_conf:
			"""未查询到代理配置"""
			raise Exception("未查询到代理服务器，请检查配置信息")
		"""生成随机数"""
		item = random.choice(proxy_server_conf)
		return item


	def get_send_msg(self, smtp_server, result):
		"""
		处理发送消息
		:param smtp_server:
		:param result:
		:return:
		"""
		"""修改标题"""
		templateFrom = BusinessUtil.replace_email_from(result.get("templateFrom"))
		fr = "%s<%s>" % (templateFrom, result.get("userName"))
		to = result.get("templateTo") if result.get("templateTo") else result.get("email")
		email_subject = result.get("templateSubject")
		templateContent = result.get("templateContent")

		"""获取邮件内容"""
		fileContent = self.get_send_email_content(result)
		msg = smtp_server.text_html_attach_msg(templateContent, fileContent)
		"""获取头部信息"""
		head_msg = smtp_server.get_header(fr, to, email_subject)
		"""更新内容信息"""
		msg['From'] = head_msg.get('From')
		msg['To'] = head_msg.get('To')
		msg['Subject'] = head_msg.get('Subject')
		msg['Date'] = head_msg.get('Date')
		msg['Message-ID'] = head_msg.get('Message-ID')
		return msg



	def get_send_email_content(self, result):
		"""
		获取邮件内容
		:param result:
		:return:
		"""
		"""获取文件路径"""
		templatePath = result.get("templatePath")
		"""读取文件内容"""
		file_content = BusinessUtil.read_file(templatePath)
		if not file_content:
			raise Exception("读取文件内容异常")
		"""替换内容参数"""
		randomNum = ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], 10))
		result["randomNum"] = randomNum
		"""邮箱加密"""
		email = result.get("email")
		secret_email = BusinessUtil.encrypt_aes(busi_config.SECRET_KEY, email)
		result["secret_email"] = secret_email
		file_content = self.replace_file_content(file_content, result)
		return file_content


	def replace_file_content(self, file_content, result):
		"""
		替换邮件内容
		:param file_content: 文件内容
		:param result: 参数
		:return:
		"""
		try:
			file_content = file_content.format(**result)
		except Exception as e:
			replace_keys = []
			[replace_keys.append(g.group(1)) for g in re.finditer("{(\w+)}", file_content)]
			for item in replace_keys:
				text = result.get(item, "")
				if not text:
					continue
				file_content = file_content.replace("{%s}" % item, text)
		finally:
			return file_content







