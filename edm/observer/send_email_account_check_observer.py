from base.observer import Observer
from exception.business_exception import BusinessExcetion
from service.send_email_account_service import SendEmailAccountService




class SendEmailAccountCheckObserver(Observer):
	"""
	账号状态检查
	"""
	def update(self):
		"""
		账号状态检查
		:return:
		"""
		"""读取账号"""
		self.logger.info("【发送邮件】0、账号状态")
		result = self.subject.email_item
		"""发送账号"""
		user_name = result.get("userName")
		"""锁定账号"""
		not_lock_user_name = SendEmailAccountService().search_not_lock_user_name(user_name)
		if not_lock_user_name:
			return
		raise BusinessExcetion("T00", "该域名已被锁定，无法发送")


if __name__ == "__main__":
	pass








