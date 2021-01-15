insert = """
	INSERT INTO `t_pop_record`(`BATCH_CODE`,`SUB_BATCH_CODE`,`MOBILE`,`EMAIL`,`SEND_ACCOUNT`,`POP3_ACCOUNT`,`SEND_SUBJECT`,`SEND_RESULT`,`RESULT_TEXT`,`RESULT_HTML`,`RESULT_ATTACH`,`STATUS`,`INTIME`,`MODTIME`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())
"""
insert_format = """
	INSERT INTO `t_pop_record`(`BATCH_CODE`,`SUB_BATCH_CODE`,`MOBILE`,`EMAIL`,`SEND_ACCOUNT`,`POP3_ACCOUNT`,`SEND_SUBJECT`,`SEND_RESULT`,`RESULT_TEXT`,`RESULT_HTML`,`RESULT_ATTACH`,`STATUS`,`INTIME`,`MODTIME`) VALUES ('{batchCode}', '{subBatchCode}', '{mobile}', '{email}', '{sendAccount}', '{pop3Account}', '{sendSubject}', '{sendResult}', '{resultText}', '{resultHtml}', '{resultAttach}', {status}, now(), now())
"""

search = """
	SELECT 
		t.RECORD_ID as recordId,
		t.BATCH_CODE as batchCode,
		t.SUB_BATCH_CODE as subBatchCode,
		t.MOBILE as mobile,
		t.EMAIL as email,
		t.SEND_ACCOUNT as sendAccount,		
		t.POP3_ACCOUNT as pop3Account,
		t.SEND_SUBJECT as sendSubject,
		t.SEND_RESULT as sendResult,
		t.RESULT_TEXT as resultText,
		t.RESULT_HTML as resultHtml,
		t.RESULT_ATTACH as resultAttach,
		t.`STATUS` as status,
		t.INTIME as intime,
		t.MODTIME as modtime
	FROM
		t_pop_record t
	WHERE
		t.`STATUS` = %s
	AND
		t.BATCH_CODE = '%s'
"""
update = """
	UPDATE t_pop_record SET `STATUS` = %s,SEND_RESULT = '%s', MODTIME = now() WHERE BOOK_ID = '%s'
"""