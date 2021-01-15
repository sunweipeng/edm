import json
import time
import traceback
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka import KafkaConsumer
from base.user_logger import UserLogger
from config import kafka_config


class KafkaProducerHelper(object):
	"""
		kafka生产者
		acks：这个参数指定了必须有多少个分区副本收到消息，生产者才会认为消息写入是成功的。这个参数对消息丢失的可能性有重要影响。
		如果acks=0；生成者在成功写入消息之前不会等待任何来自服务器的响应。也就是说，如果当中出现了问题，导致服务器没有接收到消息，那么生产者是不知道的，消息也就是丢失了。
		不过，因为生成者不需要等待服务器响应，所以它可以以网络能够支持的最大速度发送消息，从而达到很高的吞吐量。
		如果acks=1：只要集群的首领节点收到消息，生成者会收到一个来自服务器的成功响应。如果消息无法到达首领节点（比如首领节点崩溃，新的首领还没有被选举出来），生产者会收到
		一个错误响应，为了避免数据丢失，生产者会重发消息。不过，如果一个没有收到消息的节点成为新首领，消息还是会丢失。这个时候的吞吐量取决于使用的是同步发送还是异步
		发送。如果让客户端等待服务器的响应（通过调用future对象的get（）方法），显然会增加延迟。如果客户端使用回调，延迟问题可以得到缓解，不过吞吐量还是会受发送中
		消息数量的限制。
		如果acks=all，只有当所有参与复制的节点全部收到消息时，生成者才会收到一个来自服务器的成功响应。这种模式是最安全的，它可以保证不止一个服务器收到消息，就算有服务器
		发生崩溃，整个集群仍然可以运作。不过，它的延迟比acks=1时更高，因为我们要等待不只一个服务器节点接收消息。

		buffer.memory: 该参数用来设置生成者内存缓冲区的大小，生产者用它缓冲要发送到服务器的消息。如果应用程序发送消息的速度超过发送到服务器的速度，会导致生产者空间不足。
		这个时候send()方法调用要么被阻塞，要么抛出异常，取决于如何设置block.on.buffer.full参数（0.9.0.0之后的版本中被替换为max.block.ms,表示在抛出异常之
		前可以阻塞一段时间）

		compression.type: 默认情况下，消息发送不会被压缩。该参数可以设置为snappy, gzip或lz4，它指定了消息被发送给broker之前使用哪一种压缩算法进行压缩。snappy压缩，
		占用较少的CPU，却能提供较好的性能和相当可观的压缩比，如果比较关注性能和网络带宽，可以使用这种算法。gzip压缩算法一般会占用较多的CPU，但会提供更高的压缩比，
		所以如果网络带宽比较有限，可以使用这种算法。使用压缩可以降低网络传输开销和存储开销。

		retries：生成者从服务器收到的错误有可能是临时性的错误。在这种情况下，retries参数的值决定了生成者可以重发消息的次数，如果达到这个次数，生产者会放弃重试并返回错误。
		默认情况下，生产者会在每次重试之间等待100ms，不过可以通过retry.backoff.ms参数来个改变这个时间间隔。

		batch.size：当有多个消息需要被发送到同一个分区时，生产者会把它们放在同一个批次里。该参数指定了一个批次可以使用的内存大小，安装字节数计算。当批次被填满时，批次里所
		有的消息都会被发送出去。不过生产者并不一定都会等到批次填满才发送，半满的批次，甚至只包含一个消息的批次也有可能被发送。所以就算把批次带下设置得很大，也不会
		造成延迟，只是会占用更多的内存而已。但如果设置得太小，因为生产者需要更频繁地发送消息，会增加一些额外的开销。

		linger.ms :该参数指定了生产者在发送批次之前等待更多消息加入批次的时间。kafka生产者会在批次填满或者linger.ms达到上限时把批次发送出去。默认情况下，只要有可用的线程，生产者就会把消息发送出去，就算批次里只有一个消息。
		把linger.ms设置成比0大的数，让生产者在发送批次之前等待一会儿，使更多的消息加入到这个批次。虽然会增加延迟，但是会提升吞吐量（因为一次发送更多的消息，每个消息的开销变小了）

		client.id: 该参数可以是任意字符串，服务器会用它来识别消息的来源，还可以用在日志和配额指标里。

		max.in.flight.requests.per.connection: 该参数指定了生产者在收到服务器响应之前可以发送多少个消息。它的值越高，就会占用越多的内存，不过也会提升吞吐量。把它设置
		为1可以保证消息是按照发送的顺序写入服务器的，即使发生了重试。

		timeout.ms: 指定了broker等待同步副本返回消息确认的时间，与acks的配置相匹配----如果在指定时间内没有收到同步副本的确认，那么broker就会返回一个错误。

		request.timeout.ms: 指定了生产者在发送数据时等待服务器返回响应的时间。

		metadata.fetch.timeout.ms:指定了生产者在获取元数据时等待服务器返回响应的时间。如果等待响应超时，那么生产者要么重试发送数据，要么返回一个错误。

		max.block.ms: 该参数指定了在调用send()方法或使用partitionFor()方法获取元数据时生产者阻塞时间，当生产者的发送缓冲区已满，或者没有可用的元数据时，这些方法就会阻塞，
		在阻塞时间达到max.block.ms，生产者会抛出异常。

		max.request.size: 该参数用于控制生成者发送的请求大小。它可以指能发送的单个消息的最大值，也可以指单个请求里所有消息总的大小。例如，假设这个值为1MB，那么可以发送的
		单个最大消息为1MB，或者生产者可以在单个请求里发送一个批次，该批次包含了1000个消息，每个消息大小为1KB。另外，broker对可接收的消息最大值也有自己的限制，
		所以两边的配置最好可以匹配，避免生产者发送的消息被broker拒绝。

		receive.buffer.bytes和send.buffer.bytes：这两个参数分别指定了TCP socket接收和发送数据包的缓冲区大小。如果它们被设置为-1.就是用操作系统的默认值。如果生产者或
		消费者与broker处于不同的数据中心，那么可以适当增大这些值，因为跨数据中心的网络一般都有比较高的延迟和比较低的带宽。
	"""
	def __init__(self, kafka_topic="kafka_data_queue", key=None, bootstrap_servers=None):
		"""
		:param bootstrap_servers: ip地址段
		:param kafka_topic: 主题
		:param key: 根据不同key 区分消息
		"""
		"""获取kafka配置"""
		if not bootstrap_servers:
			bootstrap_servers = kafka_config.KAFKA_BOOTSTRAP_SERVERS.split(",")
		self.logger = UserLogger.getlog()
		self._bootstrap_servers = bootstrap_servers
		self._kafka_topic = kafka_topic
		self._key = key
		self._producer = KafkaProducer(bootstrap_servers=self._bootstrap_servers)

	def __producer(self):
		"""
		获取生产者对象
		:return:
		"""
		return self._producer


	def send_json_msg(self, params, kafka_topic=None, key=None):
		"""
		发送对象数据
		:param params:
		:param kafka_topic:
		:param key:
		:return:
		"""
		try:
			"""转化数据"""
			parmas_message = json.dumps(params)
			self.send_msg(parmas_message, kafka_topic, key)
		except KafkaError as e:
			self.logger.error("【kafka】发送信息：%s" % (traceback.format_exc()))
		except Exception as e:
			self.logger.error("【kafka】发送信息：%s" % (traceback.format_exc()))



	def send_msg(self, message, kafka_topic=None, key=None):
		"""
		发送普通数据
		:param message:
		:param kafka_topic:
		:param key:
		:return:
		"""
		if not kafka_topic:
			kafka_topic = self._kafka_topic
		if not key:
			key = self._key
		try:
			v = message.encode('utf-8')
			k = None
			if key:
				k = key.encode('utf-8')
			self.logger.info("【kafka】发送信息为：[topic=%s][v=%s][k=%s]" % (kafka_topic, v, k))
			self._producer.send(kafka_topic, key=k, value=v)
			self._producer.flush()
		except KafkaError as e:
			self.logger.error("【kafka】发送信息：%s" % (traceback.format_exc()))
		except Exception as e:
			self.logger.error("【kafka】发送信息：%s" % (traceback.format_exc()))



	def close(self, timeout=None):
		"""
		关闭链接
		:return:
		"""
		if not self._producer:
			return False
		self._producer.close(timeout=timeout)




class KafkaConsumerHelper(object):
	"""
		kafka消费者
		1. fetch.min.bytes：该属性指定了消费者从服务器获取记录的最小字节数。broker在收到消费者的数据请求时，如果可用的数据量小于fetch.min.bytes 指定的大小，那么它会等到
		有足够的可用数据时才把它返回给消费者。这样可以降低消费者和broker的工作负载，因为它们在主题不是很活跃的时候（或者一天里的低谷时段）就不需要来来回回地处理消息。如果没有
		很多可用数据，但消费者的CPU 使用率却很高，那么就需要把该属性的值设得比默认值大。如果消费者的数量比较多，把该属性的值设置得大一点可以降低broker 的工作负载。

		2. fetch.max.wait.ms：我们通过fetch.min.bytes告诉Kafka ，等到有足够的数据时才把它返回给消费者。而fetch.max.wait.ms 则用于指定broker 的等待时间，默认是500ms
		，如果没有足够的数据流入Kafka ，消费者获取最小数据量的要求就得不到满足，最终导致500ms 的延迟。如果要降低潜在的延迟（为了满足SLA ），可以把该参数值设置得小一些。
		如果fetch.max.wait.ms被设为lOOms ，并且fetch.min.bytes被设为1MB ，那么Kafka 在收到消费者的请求后，要么返回1MB 数据，要么在1OOms 后返回所有可用的数据，
		就看哪个条件先得到满足。

		3. max.partition.fetch.bytes:该属性指定了服务器从每个分区里返回给消费者的最大字节数。它的默认值是1MB,也就是说kafkaconsumer.poll() 方法从每个分区里返回的记录最
		多不超过max.partition.fetch.bytes指定的字节。如果一个主题有20 个分区和5 个消费者，那么每个消费者需要至少4MB 的可用内存来接收记录。在为消费者分配内存时，
		可以给它们多分配一些，因为如果群组里有消费者发生崩愤，剩下的消费者需要处理更多的分区。max.partition.fetch.bytes的值必须比broker 能够接收的最大消息的字节
		数（通过max.message.size属性配置）大， 否则消费者可能无法读取这些消息，导致消费者一直挂起重试。在设置该属性时，另一个需要考虑的因素是消费者处理数据的时间。
		消费者需要频繁调用poll()方法来避免会话过期和发生分区再均衡，如果单次调用poll()返回的数据太多，消费者需要更多的时间来处理，可能无怯及时进行下一个轮询来避免会
		话过期。如果出现这种情况， 可以把max.partition.fetch.bytes值改小，或者延长会i舌过期时间。

		4. session.timeout.ms:该属性指定了消费者在被认为死亡之前可以与服务器断开连接的时间，默认是3s 。如果消费者没有在session.timeout.ms 指定的时间内发送心跳给群组协调
		器，就被认为已经死亡，协调器就会触发再均衡，把它的分区分配给群组里的其他消费者。该属性与heartbeat.interval.ms紧密相关。heartbeat.interval.ms指定了poll()
		方法向协调器发送心跳的频率， session.timeout.ms 则指定了消费者可以多久不发送心跳。所以，一般需要同时修改这两个属性，heartbeat.interval.ms必须比
		session.timeout.ms 小， 一般是session.timeout.ms 的三分之一。如果session.timeout.ms 是3s ，那么heartbeat.interval.ms应该是1s 。
		把session.timeout.ms 值设得比默认值小，可以更快地检测和恢复崩愤的节点，不过长时间的轮询或垃圾收集可能导致非预期的再均衡。把该属性的值设
		置得大一些，可以减少意外的再均衡，不过检测节点崩愤－需要更长的时间。

		5.auto.offset.reset: 该属性指定了消费者在读取一个没有偏移量的分区或者偏移量无效的情况下（因消费者长时间失效，包含偏移量的记录已经过时井被删除）该作何处理。它的默认
		值是latest ， 意思是说，在偏移量无效的情况下，消费者将从最新的记录开始读取数据（在消费者启动之后生成的记录）。另一个值是earlist,意思是说，在偏移量无效的情况下，
		消费者将从起始位置读取分区的记录。

		6.enable.auto.commit: 该属性指定了消费者是否自动提交偏移量，默认值是true。为了尽量避免出现重复数据和数据丢失，可以把它设为false ，由自己控制何时提交偏移量。如果把
		它设为true ，还可以通过配置auto.commit.interval.ms属性来控制提交的频率。

		7.partition.assignment.strategy: 我们知道，分区会被分配给群组里的消费者。PartitionAssignor根据给定的消费者和主题，决定哪些分区应该被分配给哪个消费者。
		Kafka 有两个默认的分配策略。
		Range: 该策略会把主题的若干个连续的分区分配给消费者。假设悄费者c1 和消费者c2 同时订阅了主题t1 和主题t2 ，井且每个主题有3 个分区。那么消费者c1有可能分配到这两个主题的分区0
		和分区1 ，而消费者C2 分配到这两个主题的分区2。因为每个主题拥有奇数个分区，而分配是在主题内独立完成的，第一个消费者最后分配到比第二个消费者更多的分区。只要使用了Range
		策略，而且分区数量无怯被消费者数量整除，就会出现这种情况。 RoundRobin: 该策略把主题的所有分区逐个分配给消费者。如果使用RoundRobin 策略来给消费者c1和消费者c2 分配分区，那么消费者c1 将分到主题T1的分区0 和分区2 以及主题t2的分区1 ，消费
		者C2 将分配到主题t1 的分区1 以及主题t2的分区0 和分区2 。一般来说，如果所有消费者都订阅相同的主题（这种情况很常见） , RoundRobin 策略会给所有消费者分配相同数量的分区（或最多就差一个分区）。
		可以通过设置partition.assignment.strategy来选择分区策略。默认使用的是org.apache.kafka.clients.consumer.RangeAssignor,这个类实现了Range策略，不过也可以把
		它改为org.apache.kafka.clients.consumer.RoundRobinAssignor。还可以自定义策略，在这种情况下，partition.assignment,strategy属性的值就是自定义类的名字。

		8.client.id:该属性可以是任意字符串， broker 用它来标识从客户端发送过来的消息，通常被用在日志、度量指标和配额里。

		9.max.poll.records:该属性用于控制单次调用call() 方法能够返回的记录数量，可以帮你控制在轮询里需要处理的数据量。

		10. receive.buffer.bytes和send.buffer.bytes: socket 在读写数据时用到的TCP 缓冲区也可以设置大小。如果它们被设为-1 ，就使用操作系统的默认值。如果生产者或消费者
		与broker 处于不同的数据中心内，可以适当增大这些值，因为跨数据中心的网络一般都有比较高的延迟和比较低的带宽。
	"""
	def __init__(self, kafka_topic, bootstrap_servers=None):
		"""
		消费者初始化
		:param bootstrap_servers: ip地址段
		:param kafka_topic: 主题
		"""
		"""获取kafka配置"""
		if not bootstrap_servers:
			bootstrap_servers = kafka_config.KAFKA_BOOTSTRAP_SERVERS.split(",")
		self.logger = UserLogger.getlog()
		self._bootstrap_servers = bootstrap_servers
		self._kafka_topic = kafka_topic
		self._consumer = KafkaConsumer(self._kafka_topic, bootstrap_servers=self._bootstrap_servers)


	def consume_data(self):
		"""
		消费数据
		:return:
		"""
		try:
			for message in self._consumer:
				yield message
		except KeyboardInterrupt as e:
			self.logger.error("【kafka】消费信息：%s" % (traceback.format_exc()))
		except Exception as e:
			self.logger.error("【kafka】消费信息：%s" % (traceback.format_exc()))


	def consumer(self):
		"""获取消费对象"""
		return self._consumer



	def close(self, autocommit=True):
		"""
		关闭链接
		:return:
		"""
		if not self._consumer:
			return False
		self._consumer.close(autocommit)


if __name__ == '__main__':
	pass

