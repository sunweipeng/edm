import os



class FileHelper:
	"""
	文件工具类
	"""
	@staticmethod
	def read_in_chunks(file_path, chunk_size=1024*1024):
		"""
		分块读取文件 将大文件切割成小文件 然后读取完后释放内存
		:param file_path:
		:param chunk_size:
		:return:
		"""
		if not file_path:
			return False
		"""判断文件大小"""
		file_size = os.path.getsize(file_path)
		if file_size == 0:
			return False
		with open(file_path, "rb") as f:
			while True:
				chunk_data = f.read(chunk_size)
				if not chunk_data:
					break
				yield chunk_data


	@staticmethod
	def write_lines_2_file(file_path, lines, sub_index, suffix=None):
		"""
		按行写入文件
		:param file_path:
		:param lines:
		:param sub_index:
		:param suffix:
		:return:
		"""
		des_file_name, ext_name = os.path.splitext(file_path)
		if not suffix:
			file_name = des_file_name + '_' + str(sub_index) + ext_name
		else:
			file_name = des_file_name + '_' + str(sub_index) + '.' + suffix
		with open(file_name, 'w') as fout:
			fout.writelines(lines)
			return int(sub_index) + 1
		return ""



	@staticmethod
	def split_file_by_count(file_path, count, check_fun, encoding="utf-8", suffix=None):
		"""
		按行数切割文件
		:param file_path:
		:param count:
		:param check_fun:
		:param encoding:
		:param suffix:
		:return:
		"""
		if not file_path or not count:
			return False
		"""判断文件大小"""
		file_size = os.path.getsize(file_path)
		if file_size == 0:
			return False
		with open(file_path, "rb") as f:
			buf = []
			sub_index = 0
			for line in f:
				line_text = FileHelper.get_text_not_strip(line, encoding)
				result = check_fun(line_text)
				if result:
					buf.append(result)
				if len(buf) == count:
					sub_index = FileHelper.write_lines_2_file(file_path, buf, sub_index, suffix)
					buf = []
			if len(buf) != 0:
				sub_index = FileHelper.write_lines_2_file(file_path, buf, sub_index, suffix)
				buf = []



	@staticmethod
	def read_seek(file_path, offset=0, read_line_length=400):
		"""
		按偏移量读取文件
		:param file_path:
		:param offset:
		:param read_line_length:
		:return:
		"""
		if not file_path:
			return False
		"""判断文件大小"""
		file_size = os.path.getsize(file_path)
		if file_size == 0:
			return False
		result = list()
		current_offset = 0
		with open(file_path, "rb") as f:
			"""设置偏移量"""
			f.seek(offset)
			current_index = 0
			for line in f:
				current_index = current_index+1
				if current_index > read_line_length:
					break
				result.append(FileHelper.get_text(line))
				current_offset = f.tell()
		return {"offset": current_offset, "result": result, "file_size": file_size}



	@staticmethod
	def read_text_get_last_line(file_path):
		"""
		读取最后一行数据
		:param file_path:
		:return:
		"""
		if not file_path:
			return False
		"""判断文件大小"""
		file_size = os.path.getsize(file_path)
		if file_size == 0:
			return False
		with open(file_path, "rb") as f:
			offset = -8
			while -offset < file_size:
				f.seek(offset, 2)
				lines = f.readlines()
				if len(lines) >= 2:
					return FileHelper.get_text(lines[-1])
				else:
					offset *= 2
			f.seek(0)
			lines = f.readlines()
			return FileHelper.get_text(lines[-1])


	@staticmethod
	def get_text(text, encoding="utf-8"):
		"""
		读取文件内容
		:param text:
		:param encoding:
		:return:
		"""
		try:
			result = str(text, encoding=encoding)
		except UnicodeDecodeError:
			result = str(text, encoding='unicode_escape')
		return result.strip()


	@staticmethod
	def get_text_not_strip(text, encoding="utf-8"):
		"""
		读取文件内容，不进行回车替换
		:param text:
		:param encoding:
		:return:
		"""
		try:
			result = str(text, encoding=encoding)
		except UnicodeDecodeError:
			result = str(text, encoding='unicode_escape')
		return result

	@staticmethod
	def get_flie_list(file_dir):
		"""
		获取文件夹下文件列表
		:param file_dir:
		:return:
		"""
		L = []
		for root, dirs, files in os.walk(file_dir):
			"""生成文件数组"""
			[L.append(os.path.join(root, file)) for file in files]
		return L



	@staticmethod
	def send_email_account_init(file_dir):
		"""
		初始化发送账号sql
		:param file_dir:
		:return:
		"""
		def chekc_line(line):
			split_result = line.split(",")
			user_name = split_result[1]
			user_password = split_result[3]
			if user_name.find("@") == -1:
				return False
			email_name, domain_name = user_name.split("@")
			sql_insert_register_email = "INSERT INTO `t_send_email_account`(`DOMAIN_NAME`,`USER_NAME`,`USER_PASSWORD`,`MAX_SEND_COUNT`,`STATUS`,`INTIME`,`MODTIME`) VALUES ('{domain_name}', '{user_name}', '{user_password}', '35', 2,now(),now());\n"
			param = {
				"user_password": user_password,
				"user_name": user_name,
				"domain_name": domain_name
			}
			return sql_insert_register_email.format(**param)
		if not file_dir:
			return False
		L = FileHelper.get_flie_list(file_dir)
		if not L:
			return False
		for item in L:
			"""过滤非cvs文件"""
			if item.find("csv") == -1:
				continue
			FileHelper.split_file_by_count(item, 100, chekc_line, "gbk", "sql")




	@staticmethod
	def send_email_init(file_path):
		"""
		过滤初始化手机号
		:param file_path:
		:return:
		"""
		def chekc_line(line):
			if line.find(",") > -1:
				mobile, addrss, platform = line.split(",")
				if "北京,上海，广东".find(addrss.strip()) == -1:
					return mobile + "\n"
				return False
			return line.strip()+"\n"

		FileHelper.split_file_by_count(file_path, 100000, chekc_line)




	@staticmethod
	def search_domain_name_from_files(file_dir):
		"""
		获取所有
		:param file_dir:
		:return:
		"""
		def check_line(line):
			split_result = line.split(",")
			user_name = split_result[1]
			if user_name.find("@") == -1:
				return False
			email_name, domain_name = user_name.split("@")
			return domain_name

		def read_file(file_path, buf):
			with open(item, "rb") as f:
				for line in f:
					line_text = FileHelper.get_text_not_strip(line, "gbk")
					result = check_line(line_text)
					if result:
						buf.append(result)

		def read_server_file(file_path, buf):
			with open(item, "rb") as f:
				for line in f:
					line_text = FileHelper.get_text_not_strip(line, "gbk")
					buf.append(line_text.strip())



		if not file_dir:
			return False
		L = FileHelper.get_flie_list(file_dir)
		if not L:
			return False
		buf = []
		server_ip = []
		for item in L:
			if item.find("csv") > -1:
				read_file(item, buf)
			elif item.find("server_ip") > -1:
				read_server_file(item, server_ip)
			else:
				continue
		lines = []
		sql_init = "INSERT INTO `t_server_domian_rel`(`SERVER_IP`,`DOMAIN_NAME`,`STATUS`,`INTIME`,`MODTIME`) VALUES ('{0}','{1}',1,now(),now());\n"
		buf = list(set(buf))
		list_len = len(buf)
		server_ip_len = len(server_ip)
		for item in range(list_len):
			index = item % server_ip_len
			lines.append(sql_init.format(server_ip[index], buf[item]))
		FileHelper.write_lines_2_file(L[0], lines, 0, 'txt')








if __name__ == '__main__':
	#pass
	# FileHelper.send_email_account_init('D:\python\old\edm_old\cvs')
	# FileHelper.search_domain_name_from_files('D:\python\old\edm_old\cvs')
	# FileHelper.send_email_init('D:\python\old\edm_old\send_account\mobile.txt')
	init_num = 3
	L = FileHelper.get_flie_list(r'D:\python\old\edm_old\xinyongka')
	for item in L:
		newName = "%smobile_%s.txt" % ("D:\\python\\old\\edm_old\\xinyongka\\", init_num)
		init_num += 1
		os.rename(item, newName)




	# for item in range(8):
	# 	print(item % 6)


