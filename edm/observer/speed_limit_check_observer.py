import json
from base.observer import Observer
from util.business_util import BusinessUtil
from exception.business_exception import BusinessExcetion



class SpeedLimitCheckObserver(Observer):
	"""
	限速检查
	"""
	def update(self):
		"""
		限速检查
		:return:
		"""
		"""读取账号"""
		self.logger.info("【发送邮件】1、限速检查")
		result = self.subject.email_item
		user_name = result.get("userName")
		"""设置令牌桶"""
		self.set_token_bucket(user_name)
		"""计算令牌"""
		BusinessUtil.lock_item(user_name, user_name, consume_token, 300000, result)
		consume_result = result.get("is_smtp")
		if not consume_result:
			raise BusinessExcetion("T01", "触发限速规则")


	def set_token_bucket(self, key):
		"""
		设置令牌桶 （后续考虑到将信息添加到数据库）
		:return:
		"""
		BusinessUtil.set_token_bucket(key)



def consume_token(*keysValue):
	"""
	消费队列
	:param keysValue:
	:return:
	"""
	item = keysValue[0]
	result = BusinessUtil.get_redis_by_key(item.get("userName"))
	if type(result) == str:
		result = json.loads(result)
	"""读取令牌"""
	token_result = BusinessUtil.consume_token(result)
	if not token_result:
		item["is_smtp"] = False
	else:
		"""设置新值"""
		item["is_smtp"] = BusinessUtil.set_redis_reset_time_ex(item.get("userName"), token_result)



if __name__ == "__main__":
	pass








