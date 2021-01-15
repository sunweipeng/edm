insert = """
	INSERT INTO `t_send_record`(`BATCH_CODE`,`SUB_BATCH_CODE`,`MOBILE`,`EMAIL`,`TEMPLATE_EXT_CODE`,`SERVER_IP`,`SEND_ACCOUNT`,`STATUS`,`INTIME`,`MODTIME`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now(),now())
"""

search = """
	SELECT
		t.RECORD_ID as recordId,
		t.BATCH_CODE as batchCode,
		t.MOBILE as mobile,
		t.EMAIL as email,
		t.TEMPLATE_EXT_CODE as templateExtCode,
		t.SERVER_IP as serverIp,
		t.SEND_ACCOUNT as sendAccount,
		t.`STATUS` as status,
		t.INTIME as intime,
		t.MODTIME as modtime
	FROM
		t_send_record t
	WHERE
		t.BATCH_CODE = %s
"""

search_by_status = """
	SELECT
		COUNT(t.RECORD_ID) as num
	FROM
		t_send_record t
	WHERE
		t.SEND_ACCOUNT = %s
	AND 
		t.`STATUS` = %s
	AND 
		date(t.INTIME) = %s
"""
