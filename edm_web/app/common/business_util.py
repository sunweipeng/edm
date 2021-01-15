from Crypto.Cipher import AES
import base64


class BusinessUtil(object):
	"""
	工具类
	"""
	@staticmethod
	def add_to_16(value):
		"""
		补足16的倍数
		:param value:
		:return:
		"""
		while len(value) % 16 != 0:
			value += '\0'
		return str.encode(value)

	@staticmethod
	def encrypt_aes(key, text):
		"""
		AES加密(不支持中文)
		:param key:
		:param text:
		:return:
		"""
		aes = AES.new(BusinessUtil.add_to_16(key), AES.MODE_ECB)
		encrypt_aes = aes.encrypt(BusinessUtil.add_to_16(text))
		result = str(base64.encodebytes(encrypt_aes), encoding='utf8').replace('\n', '')
		return result

	@staticmethod
	def decrypt_aes(key, text):
		"""
		AES解密(不支持中文)
		:param key:
		:param text:
		:return:
		"""
		aes = AES.new(BusinessUtil.add_to_16(key), AES.MODE_ECB)
		base64_decrypted = base64.decodebytes(bytes(text, encoding='utf8'))
		result = str(aes.decrypt(base64_decrypted).rstrip(b'\0').decode("utf8"))
		return result


if __name__ == '__main__':
	key = "adsawdws"
	#print(BusinessUtil.encrypt_aes(key, "sunweipeng162@163.com"))
	print(BusinessUtil.decrypt_aes(key, "eXa6nEVI2A3jFrpifyN+srEYIqlvJ1uRxVhGBylXFwg="))