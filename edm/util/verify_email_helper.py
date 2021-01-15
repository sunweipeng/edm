import dns.resolver
import smtplib
import random
import requests
from base.user_logger import UserLogger
from util.business_util import BusinessUtil
from util.browser_header_helper import BrowserHeaderHelper


"""163邮箱校验"""
HTTP_CHECK_HOST_163 = {
	"163.com": "163.com",
	"126.com": "126.com",
	"vip.126.com": "vip126",
	"vip.163.com": "vip163",
	"vip.188.com": "vip188",
	"yeah.net": "yeah.net"
}
PAGE_163_URL = "https://reg.mail.163.com/unireg/call.do?cmd=register.entrance&from=163mail_right"
VERIFY_163_URL = "https://reg.mail.163.com/unireg/call.do?cmd=urs.checkName"




class VerifyEmailHelper(object):
	"""
	验证邮箱是否有效
	"""
	def __init__(self):
		"""
		初始化日志
		"""
		self.logger = UserLogger.getlog()

	def query_mx(self, host):
		"""
		1、解析邮件服务器，查找域名的 MX 记录
		:param host:
		:return:
		"""
		try:
			#self.logger.info("正在查询MX记录")
			answers = dns.resolver.query(host, 'MX')
			res = [str(item.exchange)[:-1] for item in answers]
			#self.logger.info('查找结果为：%s' % res)
			return res
		except dns.resolver.NXDOMAIN:
			self.logger.error('查询MX记录不存在')
			return False
		except Exception as e:
			self.logger.error('查询MX记录异常，异常信息为：%s' % e)
			return False


	def verify_result_status(self, retCode):
		"""
		校验返回状态
		:param retCode:
		:return:
		"""
		if retCode == 250 or retCode == 251:
			"""地址存在"""
			result_status = 1
		elif retCode > 500:
			"""地址不存在"""
			result_status = 0
		else:
			"""地址不确定是否存在"""
			result_status = -1
		return result_status




	def check_by_smtp(self, need_verify_email, verify_email, time_out=10):
		"""分割邮箱"""
		name, host = need_verify_email.split('@')
		"""查找MX记录"""
		search_mx_res = self.query_mx(host)
		if not search_mx_res:
			#self.logger.info("MX记录不存在")
			return False
		smtp_server = None
		try:
			"""连接smtp服务器"""
			smtp_host = random.choice(search_mx_res)
			#self.logger.info("开始连接smtp服务器：%s" % smtp_host)
			smtp_server = smtplib.SMTP(smtp_host, timeout=time_out)

			"""发送EHLO命令 向服务器提供连接域名"""
			verify_name, verify_host = verify_email.split("@")
			ehlo_result = smtp_server.ehlo(verify_host)
			#self.logger.info("EHLO：%s" % str(ehlo_result))
			"""验证EHLO响应结果"""
			ehlo_result_status = self.verify_result_status(ehlo_result[0])
			if ehlo_result_status < 1:
				return ehlo_result_status

			"""向邮件服务器提供邮件的来源邮箱"""
			mail_from_cmd = "MAIL FROM:<%s>" % verify_email
			send_from_result = smtp_server.docmd(mail_from_cmd)
			#self.logger.info("MAIL_FROM：%s" % str(send_from_result))
			"""验证MAIL_FROM响应结果"""
			send_from_status = self.verify_result_status(send_from_result[0])
			if send_from_status < 1:
				return send_from_status

			"""验证邮件地址是否存在"""
			rcpt_to_cmd = "RCPT TO:<%s>" % need_verify_email
			rcpt_to_result = smtp_server.docmd(rcpt_to_cmd)
			#self.logger.info("RCPT_TO：%s" % str(rcpt_to_result))
			"""校验RCPT_TO响应结果"""
			return self.verify_result_status(rcpt_to_result[0])
		except smtplib.SMTPServerDisconnected as e:
			self.logger.info("链接未关闭：%s" % e)
		except Exception as e:
			self.logger.info("链接异常：%s" % e)
		finally:
			if smtp_server:
				"""关闭链接"""
				smtp_server.close()




	def verify_email(self, need_verify_email, verify_email, time_out=10):
		"""
		验证邮箱
		:param need_verify_email: 需要验证的邮箱(不确定是否真实存在)
		:param verify_email: 验证邮箱(真实存在的)
		:param time_out:
		:return:
		"""
		if not need_verify_email or not verify_email:
			self.logger.info("请求参数为空，请确认")
			return False

		"""邮箱格式校验"""
		format_email = BusinessUtil.search_send_email(need_verify_email)
		if not format_email:
			self.logger.info("邮箱格式错误，请确认")
			return False

		"""分割邮箱"""
		name, host = need_verify_email.split('@')
		"""判断邮箱校验类型"""
		if host in HTTP_CHECK_HOST_163:
			result = self.verify_email_163(need_verify_email)
		else:
			result = self.check_by_smtp(need_verify_email, verify_email, time_out)
		return result




	def verify_email_163(self, need_verify_email):
		"""
		在线校验163邮箱有效性
		:param need_verify_email:
		:return:
		"""
		"""分割邮箱"""
		user_name, host = need_verify_email.split('@')
		"""启用session"""
		s = requests.session()
		s.headers = BrowserHeaderHelper.get_user_agent_and_content_type(1, "html")
		s.verify = True
		proxies = {
			"http": "http://218.95.81.51:9000",
			"https": None
		}
		r = s.get(PAGE_163_URL, proxies=proxies)
		"""请求页面 获取cookies"""
		if r.status_code != 200:
			"""结果不明"""
			return -1
		"""请求校验接口"""
		res = s.post(VERIFY_163_URL, data={"name": user_name}, proxies=proxies)
		if res.status_code != 200:
			"""结果不明"""
			return -1
		return_json = res.json()
		if return_json['code'] != 200:
			return -1
		if host.find("vip") > -1:
			host = host.replace(".com", "").replace(".", "")
		result = return_json.get("result").get(host, "")
		if not result:
			return 1
		else:
			return 0




if __name__ == "__main__":
	verify_result_status = VerifyEmailHelper().verify_email("18513710033@139.com", "sunweipeng16@163.com")
	print("验证邮箱结果：%s" % verify_result_status)


