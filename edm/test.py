from util.smtp_util import SMTPUtil
from util.business_util import BusinessUtil
import random
import re
import time


def get_send_msg(smtp_server, result):
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
	fileContent = get_send_email_content(result)
	#msg = smtp_server.html_attach_msg(fileContent)
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


def get_send_email_content(result):
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
	secret_email = BusinessUtil.encrypt_aes("adsawdws", email)
	result["secret_email"] = secret_email
	file_content = replace_file_content(file_content, result)
	return file_content


def replace_file_content(file_content, result):
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


if __name__ == "__main__":
	#result = {'mobile': '15058585406', 'batchCode': '2019052718505137902616269', 'originalBatchCode': '201905241427196394251011058', 'email': 'test-oz5oe@mail-tester.com', 'subBatchCode': '2019052718505164422682842', 'public_ip': '106.12.219.104', 'task_code': '201905241427196394251011058', 'domainName': 'i9bee.com', 'userName': 'mxf_i19@i9bee.com', 'userPassword': '!!!i9bee', 'smtpServer': 'smtp.i9bee.com', 'smtpPort': '465', 'smtpLoginSSL': 1, 'smtpStarttls': 0, 'residue': 100.0, 'templateCode': '20190524143550652127122710', 'templatePath': '/AppData/edm/template/zhaoshang/wangzhe.html', 'templateExtCode': '20190422200739982424746106', 'templateSubject': '招商银行金卡优选客户限时邀约', 'templateFrom': '{random_num}credit', 'templateContent': '招商银行首年免年费，生日月尊享双倍积分，全球货币0外汇兑换费，尊享海量商户会员，多款精美卡面设计，优惠折扣，超值回馈，提供吃喝玩乐一站式优惠，1分钟在线申请，72步卡片到手。', 'templateTo': None, 'serverId': 1, 'serverIp': '106.12.219.104', 'isNeedProxy': 0, 'redis_key': '201905241427196394251011058_3_pagoda_1', 'is_smtp': True}
	# result = {'batchCode': '20190611094232414013763106', 'mobile': '13607843878', 'email': 'sunweipeng16@163.com', 'level': '2', 'status': 2, 'reSendServerIp': '106.12.139.138', 'reSendAccount': 'yg12@htj2.cn', 'reSendTemplateExtCode': '2019042220073998442487673', 'originalBatchCode': '201905241427196394251011058', 'subBatchCode': '20190611095337212608138210', 'public_ip': '106.12.141.10', 'task_code': '201905241427196394251011058', 'domainName': 'htj0.cn', 'userName': 'yg33@htj0.cn', 'userPassword': 'Hello1234', 'smtpServer': 'smtp.htj0.cn', 'smtpPort': '25', 'smtpLoginSSL': 0, 'smtpStarttls': 0, 'residue': 35.0, 'templateCode': '20190524143423212373118103', 'templatePath': '/AppData/edm/template/zhaoshang/biaozhun.html', 'templateExtCode': '20190422200739976423361021', 'templateSubject': '招商银行信用卡优选客户限时权益', 'templateFrom': '{random_num}credit', 'templateContent': '招商银行首年免年费，刷卡赢1000积分，全球货币0外汇兑换费，尊享海量商户权益，4D工艺呈现多种炫酷卡面，享受高额航空意外险，提供吃喝玩乐一站式优惠，1分钟在线申请，41步卡片到手。', 'templateTo': None, 'serverId': 1, 'serverIp': '106.12.140.232', 'isNeedProxy': 0, 'redis_key': '201905241427196394251011058_1_pagoda_2'}
	# proxy_server = None
	# smtp_server = SMTPUtil(result, proxy_server)
	# """获取发送内容"""
	# smtp_msg = get_send_msg(smtp_server, result)
	# """smtp发送邮件"""
	# smtp_send_result = smtp_server.smtp_send_mail(result.get("userName"), result.get("email"), smtp_msg)
	# print(smtp_send_result)
	timeout = float(0.05)
	for i in range(10):
		print(i)
		time.sleep(timeout)
	# flag = False
	# print(int(flag))
