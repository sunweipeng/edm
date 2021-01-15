import json
import traceback
from pykafka import KafkaClient
from config import kafka_config
from base.user_logger import UserLogger



class KafkaProducerHelper(object):
	"""
	kafka生产者
	"""
	def __init__(self, host=None, zookeeper_host=None):
		"""
		初始
		:param host:
		:param zookeeper_host:
		"""
		if not host:
			host = kafka_config.KAFKA_BOOTSTRAP_SERVERS
		self.logger = UserLogger.getlog()
		self._host = host
		self._zookeeper_host = zookeeper_host
		self._client = KafkaClient(self._host)


	def send_json_msg(self, params, kafka_topic, key=None, sync=True):
		"""
		发送对象数据
		:param params:
		:param kafka_topic:
		:param key:
		:param sync: True 同步  False 异步
		:return:
		"""
		try:
			"""转化数据"""
			parmas_message = json.dumps(params)
			self.send_msg(parmas_message, kafka_topic, key, sync)
		except Exception as e:
			self.logger.error("【kafka】发送信息：%s" % (traceback.format_exc()))



	def send_msg(self, message, kafka_topic, key=None, sync=True):
		"""
		发送普通数据
		:param message:
		:param kafka_topic:
		:param key:
		:param sync:
		:return:
		"""
		try:
			"""获取主题"""
			topic = self._client.topics[kafka_topic.encode()]
			if sync:
				self.send_msg_sync(topic, message, key)
			else:
				self.send_msg_async(topic, message, key)
		except Exception as e:
			self.logger.error("【kafka】发送信息：%s" % (traceback.format_exc()))


	def send_msg_sync(self, topic, message, key):
		"""
		同步发送信息
		:param topic:
		:param message:
		:param key:
		:return:
		"""
		k = None
		if key:
			k = key.encode('utf-8')
		with topic.get_sync_producer() as producer:
			self.producer_send_data(producer, message, k)


	def send_msg_async(self, topic, message, key, delivery_reports):
		"""
		异步发送消息
		:param topic:
		:param message:
		:param key:
		:param delivery_reports:
		:return:
		"""
		k = None
		if key:
			k = key.encode('utf-8')
		with topic.get_producer(sync=False) as producer:
			self.producer_send_data(producer, message, k)



	def producer_send_data(self, producer, message, key):
		"""
		生产数据
		:param producer:
		:param message:
		:param key:
		:return:
		"""
		if isinstance(message, str):
			"""判断是否字符串"""
			v = message.encode('utf-8')
			producer.produce(v, partition_key=key)
			return

		if isinstance(message, bytes):
			"""判断是否字节数组"""
			v = message
			producer.produce(v, partition_key=key)
			return

		for item in message:
			if isinstance(item, dict):
				item = json.dumps(item)
			v = item.encode('utf-8')
			producer.produce(v, partition_key=key)


	def get_delivery_report(self, producer):
		"""
		获取报告
		:param producer:
		:return:
		"""
		return producer.get_delivery_report()

	def partitions(self, topic):
		"""
		获取分区
		:param topic:
		:return:
		"""
		return topic.partitions


	def latest_available_offsets(self, topic):
		"""
		最近可用offset
		:param topic:
		:return:
		"""
		return topic.latest_available_offsets()


	def earliest_available_offsets(self, topic):
		"""
		最早可用offset
		:param topic:
		:return:
		"""
		return topic.earliest_available_offsets()



	def held_offsets(self, consumer):
		"""
		当前消费者分区offset情况
		:param consumer:
		:return:
		"""
		return consumer.held_offsets





class KafkaConsumerHelper(object):
	"""
	kafka消费者
	"""
	def __init__(self, host=None, zookeeper_host=None):
		"""
		初始
		:param host:
		:param zookeeper_host:
		"""
		if not host:
			host = kafka_config.KAFKA_BOOTSTRAP_SERVERS
		self.logger = UserLogger.getlog()
		self._host = host
		self._zookeeper_host = zookeeper_host
		self._client = KafkaClient(self._host)


	def simple_consumer_data(self, kafka_topic, group_id):
		"""
		消费者指定消费
		:param kafka_topic:
		:param group_id:
		:return:
		"""
		try:
			"""获取主题"""
			topic = self._client.topics[kafka_topic.encode()]
			"""获取消费者"""
			consumer = topic.get_simple_consumer(consumer_group=group_id.encode(), auto_commit_enable=True, auto_commit_interval_ms=1, zookeeper_connect=self._zookeeper_host)
			"""进行消费"""
			for message in consumer:
				yield message
		except KeyboardInterrupt as e:
			self.logger.error("【kafka】消费信息：%s" % (traceback.format_exc()))
		except Exception as e:
			self.logger.error("【kafka】消费信息：%s" % (traceback.format_exc()))

	def balance_consumer_data(self, kafka_topic, group_id):
		"""
		使用balance consumer去消费kafka
		:param kafka_topic:
		:param group_id:
		:return:
		"""
		try:
			topic = self._client.topics[kafka_topic.encode()]
			"""managed = True 设置后，使用新式reblance分区方法，不需要使用zk，而False是通过zk来实现reblance的需要使用zk"""
			consumer = topic.get_balanced_consumer(consumer_group=group_id.encode(), managed=True, auto_commit_enable=True, auto_commit_interval_ms=1)
			for message in consumer:
				yield message
		except KeyboardInterrupt as e:
			self.logger.error("【kafka】消费信息：%s" % (traceback.format_exc()))
		except Exception as e:
			self.logger.error("【kafka】消费信息：%s" % (traceback.format_exc()))


	def partitions(self, topic):
		"""
		获取分区
		:param topic:
		:return:
		"""
		return topic.partitions


	def latest_available_offsets(self, topic):
		"""
		最近可用offset
		:param topic:
		:return:
		"""
		return topic.latest_available_offsets()


	def earliest_available_offsets(self, topic):
		"""
		最早可用offset
		:param topic:
		:return:
		"""
		return topic.earliest_available_offsets()



	def held_offsets(self, consumer):
		"""
		当前消费者分区offset情况
		:param consumer:
		:return:
		"""
		return consumer.held_offsets



if __name__ == '__main__':
	pass
