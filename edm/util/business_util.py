#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import os
import uuid
import random
import time
import json
import datetime
import requests
from Crypto.Cipher import AES
import hashlib
from util.redis_helper import RedisHelper
import traceback
from config import busi_config
import base64
import bisect
import math
import chardet


class BusinessUtil(object):
	"""
	工具类
	"""

	@staticmethod
	def search_mobile(text):
		"""
		获取手机号
		:param text:
		:return:
		"""
		reg = "无法发送到\s?(1[3|4|5|6|7|8|9][0-9]{9})"
		return BusinessUtil.search(reg, text)

	@staticmethod
	def search_send_result(text):
		"""
		获取发送结果
		:param text:
		:return:
		"""
		reg = "退信原因[:：]\s?(.+)"
		return BusinessUtil.search(reg, text)


	@staticmethod
	def search_send_email(text):
		"""
		邮箱校验
		:param text:
		:return:
		"""
		reg = "^[\w\-.]+@([\w]+.)+[a-z]{2,3}$"
		return BusinessUtil.search(reg, text)

	@staticmethod
	def is_email(text):
		"""
		邮箱校验
		:param text:
		:return:
		"""
		reg = "[a-z0-9.-+_]+@[a-z0-9.-+_]+.[a-z]+"
		return BusinessUtil.search(reg, text)


	@staticmethod
	def get_send_to_email(text):
		"""
		获取邮箱地址
		:param text:
		:return:
		"""
		reg = "To: (\S+)"
		return BusinessUtil.search(reg, text)

	@staticmethod
	def search(reg, text):
		"""
		正则查询
		:param reg:
		:param text:
		:return:
		"""
		if reg is None:
			return ""
		if text is None:
			return ""
		return re.findall(reg, text)

	@staticmethod
	def get_uniqu_uuid():
		"""
		通过uuid生成唯一值
		:return:
		"""
		return ''.join(str(uuid.uuid4()).split('-'))

	@staticmethod
	def get_uniqu_time():
		"""
		通过时间生成唯一值
		:return:
		"""
		return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())+''.join([str(random.randint(1, 10)) for i in range(5)])

	@staticmethod
	def get_public_ip():
		"""
		获取当期公网ip
		:return:
		"""
		s = requests.session()
		s.keep_alive = False
		req = s.get("http://txt.go.sohu.com/ip/soip")
		ip = BusinessUtil.search('\d+.\d+.\d+.\d+', req.text)
		if not ip:
			return ""
		return ip[0]


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

	@staticmethod
	def md5_str(value):
		"""
		MD5加密
		:param value:
		:return:
		"""
		m1 = hashlib.md5()
		if type(value) == bytes:
			bytes_value = value
		else:
			bytes_value = value.encode("utf-8")
		m1.update(bytes_value)
		return m1.hexdigest()

	@staticmethod
	def get_redis_by_key(key):
		"""
		读取redis信息
		:param key:
		:return:
		"""
		try:
			_redis_db = RedisHelper()
			result = _redis_db.conn.get(key)
			if result:
				return result
		except Exception as e:
			print("【redis读取】读取信息异常，异常信息为：%s" % traceback.format_exc())
		return False

	@staticmethod
	def set_redis_by_key(key, value, seconds_time):
		"""
		设置redis信息
		:param key:
		:param value:
		:param seconds_time:
		:return:
		"""
		try:
			_redis_db = RedisHelper()
			"""
			set(name, value, ex=None, px=None, nx=False, xx=False)
			ex，过期时间（秒）
			px，过期时间（毫秒）
			nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)
			xx，如果设置为True，则只有name存在时，当前set操作才执行'''
			"""
			return _redis_db.conn.set(key, json.dumps(value), ex=seconds_time, nx=True)
		except Exception as e:
			print("【redis设置】设置异常，参数为：%s,异常信息为：%s" % (str(value), traceback.format_exc()))
		return False

	@staticmethod
	def set_redis_reset_time(key, value):
		"""
		设置redis信息 过期时间 当天
		:param key:
		:param value:
		:return:
		"""
		reset_seconds = BusinessUtil.rest_of_day_seconds()
		return BusinessUtil.set_redis_by_key(key, value, reset_seconds)

	@staticmethod
	def set_redis_reset_time_ex(key, value):
		"""
		设置redis信息 过期时间 当天
		:param key:
		:param value:
		:return:
		"""
		try:
			_redis_db = RedisHelper()
			reset_seconds = BusinessUtil.rest_of_day_seconds()
			return _redis_db.conn.set(key, json.dumps(value), ex=reset_seconds)
		except Exception as e:
			print("【redis设置】设置异常，参数为：%s,异常信息为：%s" % (str(value), traceback.format_exc()))
		return False




	@staticmethod
	def delete_redis_by_key(key):
		"""
		删除redis
		:return:
		"""
		try:
			_redis_db = RedisHelper()
			return _redis_db.conn.delete(key)
		except Exception as e:
			print("【redis设置】删除异常，异常信息为：%s" % traceback.format_exc())
		return False

	@staticmethod
	def get_redis_name_by_keys(key):
		"""
		通过key获取name值列表
		:param key:
		:return:
		"""
		try:
			_redis_db = RedisHelper()
			return _redis_db.conn.keys(key)
		except Exception as e:
			print("【redis设置】获取name列表异常，异常信息为：%s" % traceback.format_exc())
		return []


	@staticmethod
	def get_redis_llen_by_key(key):
		"""
		获取队列长度
		:param key:
		:return:
		"""
		try:
			_redis_db = RedisHelper()
			return _redis_db.conn.llen(key)
		except Exception as e:
			print("【redis设置】获取队列长度异常，异常信息为：%s" % traceback.format_exc())
		return False

	@staticmethod
	def get_redis_lpop_by_key(key):
		"""
		出队列
		:param key:
		:return:
		"""
		try:
			_redis_db = RedisHelper()
			return _redis_db.conn.lpop(key)
		except Exception as e:
			print("【redis设置】出队列异常，异常信息为：%s" % traceback.format_exc())
		return False

	@staticmethod
	def get_redis_lpop_by_key_and_length(key, queue_length, max_length=10):
		"""
		出队列
		:param key: redis key值
		:param queue_length: 队列长度
		:param max_length: 读取最大个数
		:return:
		"""
		try:
			"""读取队列个数"""
			queue_length = max_length if queue_length > max_length else queue_length
			"""初始redis"""
			_redis_db = RedisHelper()
			result = []
			for index in range(queue_length):
				item = _redis_db.conn.lpop(key)
				"""追加数列"""
				result.append(item)
			"""反转"""
			#result.reverse()
			return result
		except Exception as e:
			print("【redis设置】出队列异常，异常信息为：%s" % traceback.format_exc())
		return False


	@staticmethod
	def save_file(file_path, content, model_type):
		"""
		保存文件
		:param file_path:
		:param content:
		:param model_type:
		:return:
		"""
		with open(file_path, model_type) as f:
			f.write(content)
		return True


	@staticmethod
	def get_uniq_pop_file_name(account, content, suffix, suffix_dir=None):
		if suffix_dir is None:
			suffix_dir = suffix
		_md5 = BusinessUtil.md5_str(content)
		timeStr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
		base_path = busi_config.POP_BASE_PATH % (account, timeStr, suffix_dir)
		BusinessUtil.mkdir(base_path)
		file_base_path = "%s/%s.%s" % (base_path, _md5, suffix)
		return file_base_path


	@staticmethod
	def mkdir(path):
		"""
		创建文件目录 若文件目录不存在
		:param path:
		:return:
		"""
		path = path.strip().rstrip("\\")
		if not os.path.exists(path):
			os.makedirs(path)
		return True

	@staticmethod
	def convert_data(mail_list, send_email_default="139.com", is_send_register_email=True):
		"""
		列表处理 转化拉取的数据集 默认发送139邮箱
		:param is_send_register_email:
		:param mail_list:
		:param send_email_default:
		:return:
		"""
		queue_list = []
		# 判断空条件
		if not mail_list:
			return queue_list
		# 分割邮箱数据
		send_mail_array = send_email_default.split("|")
		for it in mail_list:
			# 手机号
			mobile = it.get("mobile")
			# 注册邮箱
			register_mail = it.get("email") if is_send_register_email else ""
			email_suffix = ""
			send_mail_list = []
			if register_mail is not None and register_mail.find("@") > -1:
				# 分割邮箱
				register_arr = register_mail.split("@")
				email_suffix = register_arr[1]
				# 初始邮箱
				send_mail_list.append(register_mail)
			# 生成默认邮箱地址
			[send_mail_list.append("%s@%s" % (mobile, item)) for item in send_mail_array if email_suffix != item]
			# list set 数据互转 去重
			list_set = set(send_mail_list)
			send_mail_list = list(list_set)
			# 生成邮箱列表
			[queue_list.append({**it, "mobile": mobile, "email": item}) for item in send_mail_list]
		return queue_list

	@staticmethod
	def read_file(file_path):
		"""
		读取文件内容
		:param file_path:
		:return:
		"""
		with open(file_path, 'r', encoding='UTF-8') as f:
			info = f.read()
		return info

	@staticmethod
	def read_file_no_charset(file_path):
		"""
		读取文件内容
		:param file_path:
		:return:
		"""
		with open(file_path, 'r') as f:
			info = f.read()
		return info

	@staticmethod
	def get_msssage(message):
		"""
		获取错误信息
		:param message:
		:return:
		"""
		if not message:
			return "9999"
		exc_str = str(message)
		exc_tuple = tuple(eval(exc_str))
		retCode, retMsg, from_address = exc_tuple
		return retCode

	@staticmethod
	def parse_eml(file_path):
		"""
		解析邮件内容
		:param file_path:
		:return:
		"""
		file_info = BusinessUtil.read_file(file_path)
		"""判断内容是否为空"""
		if not file_info:
			return False
		"""读取文件内key-value"""
		keyValue = {}
		[keyValue.update({g.group(1): g.group(2)}) for g in re.finditer("(\S+): (.+)",file_info)]
		"""获取文件内容"""
		sub_content = BusinessUtil.search("Content-Type: text/html;([\S\s]*)\s{2}", file_info)
		if not sub_content:
			return False
		""""""
		[keyValue.update({"content": g.group(1).replace("\n", "")}) for g in re.finditer("Content-Transfer-Encoding: \S+\s{2}([\S\s]*)", sub_content[0])]
		"""解码"""
		keyValue["content"] = BusinessUtil.base64decode(keyValue.get("content", ""))
		return keyValue


	@staticmethod
	def base64decode(text, charset="utf-8"):
		"""
		base64解码
		:param text:
		:param charset:
		:return:
		"""
		result = base64.b64decode(text.encode(charset))
		return str(result, "utf-8")


	@staticmethod
	def parse_eml_text_param(text):
		"""
		解析文本内容
		:param text:
		:return:
		"""
		keyValue = {}
		[keyValue.update({g.group(1): g.group(2)}) for g in re.finditer("#(\S+):(\S+)#", text)]
		return keyValue

	@staticmethod
	def random_num(random_length=4, key="abcdefghijklmnopqrstuvwxyz"):
		"""

		:param random_length:
		:param key:
		:return:
		"""
		random_list = random.sample(list(key), random_length)
		return "".join(random_list)

	@staticmethod
	def replace_email_from(text):
		"""
		生成名称
		:param text:
		:return:
		"""
		keyValue = {}
		[keyValue.update({g.group(1): BusinessUtil.random_num()}) for g in re.finditer("{(\w+)}", text)]
		return text.format(**keyValue)

	@staticmethod
	def weight_choice(weight):
		"""
		加权选取随机数
		:param weight: list对应的权重序列
		:return:选取的值在原列表里的索引
		"""
		weight_sum = []
		total = 0
		for a in weight:
			total += a
			weight_sum.append(total)
		if total == 0:
			return -1
		t = random.randint(0, total - 1)
		return bisect.bisect_right(weight_sum, t)

	@staticmethod
	def lock_item(key, value, fun, timeout=300000, *keysValue):
		"""
		redis 加锁解锁
		:param key: 加锁key值
		:param value:
		:param fun: 执行方法
		:param timeout: 过期时间 (毫秒) 默认5分钟
		:return:
		"""
		"""加锁 查看存在状态  若存在 则不存在则新增并返回1 若不存在 则返回0"""
		try:
			key = "%s_%s" % (key, "key")
			_redis_db = RedisHelper()
			result = _redis_db.lock_item(key, value, fun, timeout, *keysValue)
			return result
		except Exception as e:
			print("【redis设置】加锁异常，异常信息为：%s" % traceback.format_exc())
		return False

	@staticmethod
	def rest_of_day_microseconds():
		"""
		截止到目前当日剩余时间 毫秒
		:return:
		"""
		today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
		tomorrow = today + datetime.timedelta(days=1)
		nowTime = datetime.datetime.now()
		return (tomorrow - nowTime).microseconds  # 获取毫秒值


	@staticmethod
	def rest_of_day_seconds():
		"""
		截止到目前当日剩余时间 秒
		:return:
		"""
		today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
		tomorrow = today + datetime.timedelta(days=1)
		nowTime = datetime.datetime.now()
		return (tomorrow - nowTime).seconds  # 获取秒

	@staticmethod
	def set_token_bucket(key, result=None):
		"""
		设置令牌桶 （后续考虑到将信息添加到数据库）
		:return:
		"""
		value = {
			"rate": 0.25,
			"capacity": 4,
			"current_token": 1,
			"last_consume_time": int(time.time())
		}
		"""如果传入参数非空 合并对象"""
		if result:
			value.update(result)
		"""key值存在则 则不更新 反之则初始化"""
		return BusinessUtil.set_redis_reset_time(key, value)



	@staticmethod
	def consume_token(result, token=1):
		"""
		消费令牌
		:param result:
		:param token:
		:return:
		"""
		rate = float(result.get("rate"))
		capacity = int(result.get("capacity"))
		current_token = int(result.get("current_token"))
		last_consume_time = int(result.get("last_consume_time"))
		increment = math.floor((int(time.time()) - last_consume_time) * rate)
		"""计算桶容量 令牌容量不得超过桶容量"""
		current_token = min(increment + current_token, capacity)
		"""当不存在可用令牌时，暂停发送"""
		if token > current_token:
			return False
		"""更新上次令牌发送时间"""
		last_consume_time = int(time.time())
		"""消费令牌"""
		current_token -= token
		return {
			"rate": rate,
			"capacity": capacity,
			"current_token": current_token,
			"last_consume_time": last_consume_time
		}

	@staticmethod
	def div_list(ls, n):
		"""
		分割列表
		:param ls: 列表
		:param n: 分割次数
		:return:
		"""
		if not isinstance(ls, list) or not isinstance(n, int):
			return []
		ls_result = []
		length = len(ls)
		if length % n == 0:
			step = int(length / n)
			[ls_result.append(ls[i: i + step]) for i in range(0, length, step)]
		elif length < n:
			[ls_result.append(ls[i: i + 1]) for i in range(0, length, 1)]
		else:
			last_step = length % n
			first_list = ls[0:length-last_step]
			first_length = len(first_list)
			first_step = int(first_length / n)
			[ls_result.append(ls[i: i + first_step]) for i in range(0, first_length, first_step)]
			last_list = ls[-last_step:]
			for i in range(last_step):
				ls_result[i].append(last_list[i])
		return ls_result

	@staticmethod
	def detect(text, encoding="utf-8"):
		"""
		解码文件
		:param text:
		:param encoding:
		:return:
		"""
		decode_text = ""
		if type(text) == bytes:
			encoding = chardet.detect(text).get("encoding")
		try:
			decode_text = decode_text.decode(encoding)
		except UnicodeDecodeError:
			decode_text = decode_text
		return decode_text



	@staticmethod
	def get_verify_key(email, default_key="_verify", default_delivery=1000):
		"""
		获取redis key值
		:param email:
		:param default_key:
		:param default_delivery:
		:return:
		"""
		if email.find("@") == -1:
			return False
		user_name, host = email.split('@')
		char_list = [str(ord(item)) for item in user_name if item.isalnum()]
		_num = int("".join(char_list)) % default_delivery
		return "%s%s" % (_num, default_key)




if __name__ == '__main__':
	# content = BusinessUtil.parse_eml("D:\AppData\edm\pop3\\2.eml")
	# print(content.get("content"))
	# result = BusinessUtil.parse_eml_text_param(content.get("content"))
	# print(result)
	def sort_key(key):
		taskCode, server_index, name, index = key.split("_")
		return index

	list_second = [
		"201905241427196394251011058_1_pagoda_1",
		"201905241427196394251011058_1_pagoda_2",
		"201905241427196394251011058_1_pagoda_3",
		"201905241427196394251011058_2_pagoda_1",
		"201905241427196394251011058_3_pagoda_1"
	]
	list_second.sort(key=sort_key)

	list_first = ["201905241427196394251011058_2_pagoda_1"]
	list_new = list_first + list_second

	print(list_new)


	pass


