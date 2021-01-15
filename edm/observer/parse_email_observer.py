#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from util.business_util import BusinessUtil




class ParseEmailObserver(Observer):

	"""
	解析邮件内容
	"""
	def update(self):
		"""
		解析邮件内容
		:return:
		"""
		result = self.subject.pop3_result
		"""判断结果"""
		if not result:
			return
		"""解析邮件内容"""
		for item in result:
			"""解析退信内容 获取 sendResult"""
			parseTextResult = self.parseText(item)
			self.logger.info("解析退信内容结果为：%s" % parseTextResult)
			"""解析eml内容 获取 mobile、batchCode、subBatchCode、templateCode"""
			parseEMLResult = self.parseEML(item)
			self.logger.info("解析eml内容结果为：%s" % parseEMLResult)
			if not parseEMLResult.get("mobile"):
				"""解析HTML内容 获取 mobile、batchCode、subBatchCode、templateCode"""
				parseEMLResult = self.parseHtml(item)
				self.logger.info("解析HTML内容结果为：%s" % parseEMLResult)
			"""更新记录"""
			item.update(parseTextResult)
			item.update(parseEMLResult)


	def parseHtml(self, item):
		"""
		解析退信内容 获取mobile、batchCode、subBatchCode、templateCode
		:param item:
		:return:
		"""
		result = {"sendResult": item.get("sendSubject", ""), "mobile": "", "batchCode": "", "subBatchCode": "", "templateCode": "", "email": ""}
		html_path = item.get("resultHtml", "")
		"""文件是否存在 或后缀名不正确"""
		if not html_path or html_path.find("html") < 0:
			return result
		"""读取内容"""
		file_info = BusinessUtil.read_file(html_path)
		"""判断内容是否为空"""
		if not file_info:
			return result
		"""解析数据"""
		parse_text_result = BusinessUtil.parse_eml_text_param(file_info)
		"""更新"""
		result.update(parse_text_result)
		return result



	def parseText(self, item):
		"""
		解析退信内容 获取sendResult
		:param item:
		:return:
		"""
		result = {"sendResult": ""}
		text_path = item.get("resultText", "")
		"""文件是否存在"""
		if not text_path:
			return result
		"""读取文件内容"""
		text_content = BusinessUtil.read_file(text_path)
		"""解析"""
		sendResult = BusinessUtil.search_send_result(text_content)
		"""结果不为空"""
		if sendResult:
			result["sendResult"] = sendResult[0].strip()
		return result


	def parseEML(self, item):
		"""
		解析eml后缀文件 获取mobile、batchCode、subBatchCode、templateCode
		:param item:
		:return:
		"""
		result = {"mobile": "", "batchCode": "", "subBatchCode": "", "templateCode": "", "email": ""}
		eml_path = item.get("resultAttach", "")
		"""文件是否存在 或后缀名不正确"""
		if not eml_path or eml_path.find("eml") < 0:
			return result
		"""解析邮件内容"""
		parse_eml_result = BusinessUtil.parse_eml(eml_path)
		"""获取发送账号"""
		result.update({"email": parse_eml_result.get("To")})
		"""获取文件内容"""
		parse_content = parse_eml_result.get("content")
		"""解析数据"""
		parse_text_result = BusinessUtil.parse_eml_text_param(parse_content)
		"""更新"""
		result.update(parse_text_result)
		return result


if __name__ == "__main__":
	ParseEmailObserver().update()

