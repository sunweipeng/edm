#!/usr/bin/python3
# -*- coding: utf-8 -*-
import poplib
from email.header import decode_header, Header
from email.utils import parseaddr
from util.business_util import BusinessUtil
import email
import traceback
from base.user_logger import UserLogger
import chardet



class POP3Util(object):
	"""
	拉取邮件
	"""
	def __init__(self, pop3_server):
		"""
		初始化pop_server
		"""
		self.logger = UserLogger.getlog()
		self._server = self._get_server(pop3_server)

	# def __del__(self):
	# 	"""
	# 	销毁实例
	# 	:return:
	# 	"""
	# 	self.close()

	def _get_server(self, pop3_server):
		"""
		初始化server
		:param is_ssl:
		:param pop3_server:
		:return:
		"""
		if int(pop3_server.get("pop3LoginSSL", "0")):
			server = poplib.POP3_SSL(pop3_server.get("pop3Server"), int(pop3_server.get("pop3Port")), timeout=30)
		else:
			server = poplib.POP3(pop3_server.get("pop3Server"), int(pop3_server.get("pop3Port")), timeout=30)
		server.user(pop3_server.get("userName"))
		server.pass_(pop3_server.get("userPassword"))
		return server

	def close(self):
		"""
		关闭链接
		:return:
		"""
		if self._server:
			self._server.close()

	def del_email_by_index(self, index):
		"""
		通过索引删除邮件
		:param index:
		:return:
		"""
		if self._server:
			self._server.dele(index)


	def decode_str(self, s):
		"""
		邮件头解码
		:param s:
		:return:
		"""
		value, charset = decode_header(s)[0]
		if charset:
			value = value.decode(charset)
		return value


	def get_header(self, message):
		"""
		header解析
		:param message:
		:return:
		"""
		result = {}
		title = None
		for header in ['From', 'To', 'Subject']:
			value = message.get(header, "")
			if value:
				if header == "Subject":
					value = self.decode_str(value)
					title = "sendSubject"
				elif header == "From":
					hdr, addr = parseaddr(value)
					name = self.decode_str(hdr)
					value = u'%s <%s>' % (name, addr)
					title = "sendAccount"
				else:
					hdr, addr = parseaddr(value)
					value = addr
					title = "pop3Account"
			result[title] = value
		return result


	def get_file_name(self, message):
		"""
		获取邮件附件名称
		:param message:
		:return:
		"""
		file_name = message.get_filename()
		header = Header(file_name)
		dh = decode_header(header)
		filename = dh[0][0]
		if dh[0][1]:
			filename = self.decode_str(str(filename, dh[0][1]))
		return filename


	def process_message(self, account, msg, resultText):
		"""
		解析邮件正文
		:param account:
		:param msg:
		:param resultText:
		:return:
		"""
		try:
			if msg.is_multipart():
				for part in msg.get_payload():
					self.process_message(account, part, resultText)
			else:
				content_type = msg.get_content_type()
				if content_type == 'text/plain':
					content = msg.get_payload(decode=True)
					# 要检测文本编码:
					charset = msg.get_content_charset(msg)
					if charset:
						content = content.decode(charset)
					file_path = BusinessUtil.get_uniq_pop_file_name(account, content, 'txt')
					BusinessUtil.save_file(file_path, content, 'w+')
					resultText["resultText"] = file_path
				elif content_type == 'text/html':
					content = msg.get_payload(decode=True)
					# 要检测文本编码:
					charset = msg.get_content_charset(msg)
					if charset:
						content = content.decode(charset)
					file_path = BusinessUtil.get_uniq_pop_file_name(account, content, 'html')
					BusinessUtil.save_file(file_path, content, 'w+')
					resultText["resultHtml"] = file_path
				else:
					# 不是文本,作为附件处理:
					file_name = self.get_file_name(msg)
					# 获取后缀
					suffix = file_name.split(".")[1]
					content = msg.get_payload(decode=True)
					file_path = BusinessUtil.get_uniq_pop_file_name(account, content, suffix, 'attach')
					BusinessUtil.save_file(file_path, content, 'wb')
					resultText["resultAttach"] = file_path
		except Exception as e:
			self.logger.info("解析邮件失败：%s" % (traceback.format_exc()))


	def pop3_email(self, pop_accout):
		"""
		收取邮件
		:param pop_accout:
		:return:
		"""
		result = []
		try:
			if not self._server:
				return
			resp, mails, objects = self._server.list()
			mailSize = len(mails)
			"""内容列表为空 直接返回"""
			if mailSize == 0:
				return
			"""收取邮件"""
			for i in range(1, mailSize + 1):
				try:
					# 解析单个邮件
					resp, lines, octets = self._server.retr(i)
					msg_content = b'\r\n'.join(lines).decode()
					msg = email.message_from_string(msg_content)
					# 解析邮件头
					header = self.get_header(msg)
					# 解析邮件内容
					resultText = {"resultText": "", "resultHtml": "", "resultAttach": ""}
					self.process_message(pop_accout, msg, resultText)
					Z = {**header, **resultText}
					result.append(Z)
				except Exception as e:
					self.logger.info("%s接收第%d封邮件失败%s" % (pop_accout, i, traceback.format_exc()))
		except Exception as e:
			self.logger.info("%s接收第%d封邮件失败%s" % (pop_accout, i, traceback.format_exc()))
		finally:
			self.close()
			return result

	def del_email(self, pop_accout):
		"""
		删除邮件
		:param pop_accout:
		:return:
		"""
		resp, mails, objects = self._server.list()
		mailSize = len(mails)
		"""内容列表为空 直接返回"""
		if mailSize == 0:
			return False
		for i in range(1, mailSize + 1):
			try:
				self._server.dele(i)
			except Exception as e:
				self.logger.info("%s删除第%d封邮件失败：%s" % (pop_accout, i, traceback.format_exc()))
		self.close()



if __name__ == "__main__":
	pass
