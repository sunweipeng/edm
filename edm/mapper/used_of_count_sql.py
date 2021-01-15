search = """
	SELECT 
		t.USED_OF_ID as userOfId,
		t.USED_CONTENT as usedOfContent,
		t.USED_TYPE as usedType,
		t.USED_COUNT as usedCount,
		t.SELECT_COUNT as selectCount
	FROM t_used_of_count t
	WHERE
		t.USED_CONTENT = %s
	AND 
		t.USED_TYPE = %s
	AND
		t.INTIME >= %s
	AND 
		t.INTIME <= %s
"""

search_account_residue = """
	SELECT	
		a.MAX_SEND_COUNT as maxSendCount,
		(a.MAX_SEND_COUNT-IFNULL(c.SELECT_COUNT,0)) as residue
	FROM
		t_send_email_account a
	LEFT JOIN
		t_send_email_conf b
	ON
		a.DOMAIN_NAME = b.DOMAIN_NAME
	LEFT JOIN
		t_used_of_count c
	ON
		c.USED_CONTENT = a.USER_NAME 
	AND 
		date(c.INTIME) = %s
	WHERE
		a.`STATUS` = 1
	AND 
		a.USER_NAME = %s
"""


search_by_type = """
	SELECT 
		b.USER_NAME as userName,
		b.USER_PASSWORD as userPassword,
		c.POP3_SERVER as pop3Server,
		c.POP3_PORT as pop3Port,
		c.POP3_LOGIN_SSL as pop3LoginSSL
	FROM 
		t_used_of_count a 
	INNER JOIN
		t_send_email_account b
	ON
		b.USER_NAME = a.USED_CONTENT
	LEFT JOIN
		t_send_email_conf c
	ON
		b.DOMAIN_NAME = c.DOMAIN_NAME
	WHERE 
		a.USED_TYPE=2
	AND
		a.INTIME >= %s
	AND
		a.INTIME <= %s
"""

count = """
	SELECT 
		t.USED_OF_ID
	FROM t_used_of_count t
	WHERE
		t.USED_CONTENT = %s
	AND 
		t.USED_TYPE = %s
	AND
		t.INTIME >= %s
	AND 
		t.INTIME <= %s
"""



update_used_count = """
	UPDATE t_used_of_count SET `USED_COUNT` = USED_COUNT+1,MODTIME = now() WHERE USED_CONTENT in (%s,%s,%s) AND INTIME >= %s AND INTIME <= %s
"""

update_select_count = """
	UPDATE t_used_of_count SET `SELECT_COUNT` = SELECT_COUNT+1,MODTIME = now() WHERE USED_CONTENT = %s AND USED_TYPE= %s AND INTIME >= %s AND INTIME <= %s
"""

insert = """
	INSERT INTO `t_used_of_count`(`USED_CONTENT`,`USED_TYPE`,`USED_COUNT`,`SELECT_COUNT`,`STATUS`,`INTIME`,`MODTIME`) VALUES (%s, %s, 0, 1, 1, now(),now())
"""

insert_used = """
	INSERT INTO `t_used_of_count`(`USED_CONTENT`,`USED_TYPE`,`USED_COUNT`,`SELECT_COUNT`,`STATUS`,`INTIME`,`MODTIME`) VALUES (%s, %s, 1, 1, 1, now(),now())
"""

update_used_count = """
	UPDATE t_used_of_count SET `USED_COUNT` = USED_COUNT+1,MODTIME = now() WHERE USED_CONTENT = %s AND USED_TYPE= %s AND INTIME >= %s AND INTIME <= %s
"""

update_used_subtract = """
	UPDATE t_used_of_count SET `SELECT_COUNT` = SELECT_COUNT-1,MODTIME = now() WHERE USED_CONTENT = %s AND USED_TYPE= %s AND INTIME >= %s AND INTIME <= %s
"""
