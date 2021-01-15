#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import socks
import smtplib
from email.header import Header
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr, formatdate, make_msgid
from util.business_util import BusinessUtil
import traceback
from base.user_logger import UserLogger


class SMTPUtil(object):
	"""
	邮件SMTP发送工具类
	"""
	def __init__(self, smtp_server, proxy_server=None):
		"""
		初始化smtp_server
		:param smtp_server:
		:param proxy_server:
		"""
		self._server = None
		self.logger = UserLogger.getlog()
		self._server = self._get_server(smtp_server, proxy_server)



	# def __del__(self):
	# 	"""
	# 	关闭服务
	# 	:return:
	# 	"""
	# 	self.close()
	def _get_server(self, smtp_server, proxy_server=None):
		"""
		获取smtp_server
		:param smtp_server:
		:param proxy_server:
		:return:
		"""
		if proxy_server:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_server.get("proxyServerIp"),
								  int(proxy_server.get("proxyServerPort")),
								  True, proxy_server.get("userName"), proxy_server.get("userPassword"))
			socks.wrapmodule(smtplib)
		if int(smtp_server.get("smtpLoginSSL", "0")):
			server = smtplib.SMTP_SSL(smtp_server.get("smtpServer"), int(smtp_server.get("smtpPort")), timeout=30)
			server.ehlo()
		else:
			server = smtplib.SMTP(smtp_server.get("smtpServer"), int(smtp_server.get("smtpPort")), timeout=30)
		'''是否安全文本传输协议'''
		if smtp_server.get("smtpStarttls", "0"):
			server.starttls()
		# 认证用户
		server.login(smtp_server.get("userName"), smtp_server.get("userPassword"))
		return server


	def smtp_send_mail(self, fr, to, msg):
		"""
		发送邮件
		:param fr:
		:param to:
		:param msg:
		:return:
		"""
		retCode = None
		retMsg = None
		try:
			# 发送邮件
			send_code = self._server.sendmail(fr, to, msg.as_string())
			self.logger.info("SMTP发送邮件返回码为：%s" % send_code)
			retCode = 1
		except smtplib.SMTPConnectError as e:
			self.logger.info("SMTP连接异常，异常信息为：%s" % e)
			retCode = e.smtp_code
			retMsg = e.smtp_error
		except smtplib.SMTPDataError as e:
			self.logger.info("SMTP数据异常，异常信息为：%s" % e)
			retCode = e.smtp_code
			retMsg = e.smtp_error
		except smtplib.SMTPAuthenticationError as e:
			self.logger.info("SMTP登录异常，异常信息为：%s" % e)
			retCode = e.smtp_code
			retMsg = e.smtp_error
		except smtplib.SMTPException as e:
			self.logger.info("SMTP其他异常，异常信息为：%s" % e)
			retCode = e.smtp_code
			retMsg = e.smtp_error
		except Exception as e:
			self.logger.info("SMTP发送邮件异常，异常信息为：%s" % traceback.format_exc())
			retCode = 0
			retMsg = "发送异常"
		finally:
			self.close()
			return {"retCode": retCode, "retMsg": retMsg}


	def close(self):
		"""
		关闭SMTP服务
		:return:
		"""
		if self._server:
			self._server.close()

	def _format_addr(self, value):
		"""
		解析数据
		:param value:
		:return:
		"""
		name, addr = parseaddr(value)
		return formataddr((Header(name, 'utf-8').encode(), addr))

	def get_header(self, fr, to, subject):
		"""
		设置邮件头部

		:param fr:
		:param to:
		:param subject:
		:return:
		"""
		return {
			"From": self._format_addr(fr),
			"To": self._format_addr(to),
			"Subject": Header(subject, 'utf-8').encode(),
			"Date": formatdate(localtime=True),
			"Message-ID": make_msgid()
		}


	def html_attach_msg(self, html):
		"""
		发送HTML
		:return:
		"""
		email = MIMEMultipart()
		content = MIMEText(html, 'html', 'utf-8')
		email.attach(content)
		return email

	def text_attach_msg(self, text):
		"""
		发送文本内容
		:param text:
		:return:
		"""
		email = MIMEMultipart()
		content = MIMEText(text, 'plain', 'utf-8')
		email.attach(content)
		return email

	def text_html_attach_msg(self, text, html):
		"""
		发送HTML及文本内容
		:param text:
		:param html:
		:return:
		"""
		email = MIMEMultipart('alternative')
		content = MIMEText(text, 'plain', 'utf-8')
		email.attach(content)
		html_str = MIMEText(html, 'html', 'utf-8')
		email.attach(html_str)
		return email

	def image_attach_msg(self, file_path):
		"""
		发送图片
		:param file_path:
		:return:
		"""
		if file_path is None:
			return False
		filename = os.path.basename(file_path)
		suffix = filename.split(".")[1]
		return self.file_attach_msg(file_path, 'image', suffix)


	def file_attach_msg(self, file_path, maintype='application', subtype="octet-stream"):
		"""
		发送附件
		:param file_path:
		:param maintype:
		:param subtype:
		:return:
		"""
		email = MIMEMultipart()
		with open(file_path, 'rb') as f:
			mime = MIMEBase(maintype, subtype, filename=f.name)
			mime.add_header('Content-Disposition', 'attachment', filename=f.name)
			mime.add_header('Content-ID', '<0>')
			mime.add_header('X-Attachment-Id', '0')
			# 把附件的内容读进来:
			mime.set_payload(f.read())
			# 用Base64编码:
			encoders.encode_base64(mime)
			email.attach(mime)
		return email





if __name__ == "__main__":
	pass
