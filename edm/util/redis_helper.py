#!/usr/bin/python3
# -*- coding: utf-8 -*-
import redis
import json
from config import redis_config
from base import global_argument

"""
redis工具类
"""
set_config = {**redis_config.redis_config}


class RedisHelper(object):
	__pool = None
	__conn = None

	def __init__(self, pooled=True):
		"""
		初始化
		:param pooled:
		"""
		self._conn = RedisHelper.__get_conn(pooled)

	@property
	def conn(self):
		return self._conn

	@classmethod
	def __get_conn(cls, pooled=True):
		"""
		获取redis连接
		:param pooled:
		:return:
		"""
		"""获取公网IP"""
		public_ip = global_argument.get_value()
		if public_ip == set_config.get("host"):
			set_config["host"] = "127.0.0.1"
		if pooled:
			if RedisHelper.__pool is None:
				RedisHelper.__pool = redis.ConnectionPool(**set_config)
			return redis.Redis(connection_pool=RedisHelper.__pool)
		else:
			if RedisHelper.__conn is None:
				RedisHelper.__conn = redis.Redis(**set_config)
			return RedisHelper.__conn


	def publish(self, channel, msg):
		"""
		发布
		:param channel:
		:param msg:
		:return:
		"""
		self._conn.publish(channel,	msg)
		return True


	def subscribe(self, channel):
		"""
		订阅
		:param channel:
		:return:
		"""
		pub = self._conn.pubsub()
		pub.subscribe(channel)
		pub.parse_response()
		return pub


	def lpush_list(self, arrList, channel):
		"""
		入队列操作 list
		:param arrList:
		:param channel:
		:return:
		"""
		if arrList is None:
			return False
		for item in arrList:
			self._conn.lpush(channel, json.dumps(item))
		return True

	def lpush_item(self, item, channel):
		"""
		入队列操作 item
		:param item:
		:param channel:
		:return:
		"""
		if item is None:
			return False
		self._conn.lpush(channel, json.dumps(item))
		return True


	def lock_item(self, key, value, fun, timeout=300000, *keysValue):
		"""
		redis 加锁解锁
		:param key: 加锁key值
		:param value:
		:param fun: 执行方法
		:param timeout: 过期时间 (毫秒) 默认5分钟
		:return:
		"""
		"""加锁 查看存在状态  若存在 则不存在则新增并返回1 若不存在 则返回0"""
		status = self._conn.set(key, value, px=timeout, nx=True)
		"""判断状态"""
		if not status:
			return False
		"""执行对应方法"""
		if hasattr(fun, '__call__'):
			fun(*keysValue)
		"""解锁"""
		"""lua脚本"""
		script = "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) else return 0 end"
		result = self._conn.eval(script, 1, key, value)
		return result


if __name__ == "__main__":
	pass

