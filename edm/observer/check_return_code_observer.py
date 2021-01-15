#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from service.return_code_conf_service import ReturnCodeConfService
from service.send_record_service import SendRecordService
from util.business_util import BusinessUtil
from config import busi_config




class CheckReturnCodeObserver(Observer):
	"""
	返回码检查
	"""
	def update(self):
		"""
		返回码检查 触发规则 执行返回码规则 并清空账号redis
		:return:
		"""
		self.logger.info("【发送邮件】3、返回码检查")
		result = self.subject.email_item
		"""返回码数据"""
		send_status = result.get("send_status")
		"""判断发送结果"""
		if int(send_status) <= 1:
			return
		return_code_list = ReturnCodeConfService().search_key(send_status)
		"""查询返回码 是否配置相关返回码信息"""
		if not return_code_list:
			return
		"""返回码"""
		return_code = return_code_list[0]
		"""策略"""
		policy_sql = return_code.get("policy")
		if not policy_sql:
			return

		user_name = result.get("userName")

		"""特殊返回码 554（3,4）说明 更新为3表示延迟重试更新  更新为4表示24小时后重试"""
		if int(send_status) == 554:
			"""查询当前账号554发生个数大于2次更新为状态4 表示24小时后重试  反之稍后重试"""
			send_record_result = SendRecordService().search_by_status(user_name, send_status)
			if int(send_record_result) >= 1:
				result["record_status"] = 4
			else:
				result["record_status"] = 3
				# """判断剩余量"""
				# residue_num = UsedOfCountService().search_account_residue(user_name)
				# if int(residue_num) < 5:
				# 	result["record_status"] = 4
				# else:
				# 	result["record_status"] = 3
		self.logger.info("【发送邮件】触发返回码规则[%s]，进行规则修改" % send_status)
		policy_sql = policy_sql.format(**result)
		"""通过策略语句操作数据"""
		ReturnCodeConfService().update_by_policy(policy_sql)
		"""清空有效账号redis"""
		valid_account = "*_%s" % busi_config.VALID_ACCOUNT_REDIS_KEY
		BusinessUtil.delete_redis_by_key(valid_account)





if __name__ == "__main__":
	pass







