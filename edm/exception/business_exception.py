

class BusinessExcetion(Exception):
	"""
	自定义错误信息
	"""
	def __init__(self, code, msg):
		"""
		自定义错误信息
		:param code:
		:param msg:
		"""
		self.retCode = code
		self.retMsg = msg
		self.args = (code, msg)
