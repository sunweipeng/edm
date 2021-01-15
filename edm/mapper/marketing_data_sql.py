insert = """
	INSERT INTO `t_marketing_data`(`ORIGINAL_BATCH_CODE`,`BATCH_CODE`,`SUB_BATCH_CODE`,`MOBILE`,`EMAIL`,`STATUS`,`INTIME`,`MODTIME`) VALUES (%s, %s, %s, %s, %s, %s, now(),now())
"""
count = """
	SELECT 
		t.MARKETING_DATA_ID
	FROM
		t_marketing_data t
	WHERE
		t.BATCH_CODE = %s
	AND
		t.MOBILE = %s
	AND
		t.EMAIL = %s
"""

search = """
	SELECT 
		t.MARKETING_DATA_ID as marketingDataId,
		t.BATCH_CODE as batchCode,
		t.SUB_BATCH_CODE as subBatchCode,
		t.MOBILE as mobile,
		t.EMAIL as email,
		t.SEND_COUNT as sendCount,
		t.SEND_RESULT as sendResult,
		t.`STATUS` as status,
		t.INTIME as intime,
		t.MODTIME as modtime
	FROM
		t_marketing_data t
	WHERE
		t.`STATUS` = %s
	AND
		t.BATCH_CODE = %s

"""

resend_search = """
	SELECT 
		a.BATCH_CODE as batchCode,
		a.MOBILE as mobile,
		a.EMAIL as email,
		CONCAT(a.SEND_COUNT+1) as level,
		a.`STATUS` as status,
		b.reSendServerIp,
		b.reSendAccount,
		b.reSendTemplateExtCode,
		a.ORIGINAL_BATCH_CODE as originalBatchCode
	FROM 
		t_marketing_data a
	LEFT JOIN
	(
		SELECT 
		t.MOBILE,
		t.EMAIL,
		group_concat(DISTINCT t.SERVER_IP) as reSendServerIp, 
		group_concat(DISTINCT t.SEND_ACCOUNT) as reSendAccount, 
		group_concat(DISTINCT t.TEMPLATE_EXT_CODE) as reSendTemplateExtCode 
		from t_send_record t
		GROUP BY t.MOBILE,t.EMAIL
	) b
	ON
		a.MOBILE = b.MOBILE AND a.EMAIL = b.EMAIL
	WHERE 
		a.`STATUS` in (2)
	AND
		a.SEND_COUNT >= 1
	AND
		a.ORIGINAL_BATCH_CODE = %s
	AND
		a.SEND_COUNT < %s
"""



update_insert = """
	UPDATE t_marketing_data SET SUB_BATCH_CODE = %s,`STATUS` = %s, SEND_COUNT =SEND_COUNT+1,MODTIME = now() WHERE BATCH_CODE = %s AND MOBILE = %s AND EMAIL = %s
"""

update_status = """
	UPDATE t_marketing_data SET `STATUS` = %s,`SEND_RESULT` = NULL, MODTIME = now() WHERE BATCH_CODE = %s AND MOBILE = %s AND EMAIL = %s
"""

update = """
	UPDATE t_marketing_data SET `STATUS` = %s,`SEND_RESULT` = %s, MODTIME = now() WHERE EMAIL = %s
"""