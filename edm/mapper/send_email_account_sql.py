search = """
	SELECT
		a.ACCOUNT_ID as accountId,
		a.DOMAIN_NAME as domainName,
		a.USER_NAME as userName,
		a.USER_PASSWORD as userPassword,
		a.MAX_SEND_COUNT as maxSendCount,
		a.`STATUS` as status,
		b.CONF_ID as confId,
		b.SMTP_SERVER as smtpServer,
		b.POP3_SERVER as pop3Server,
		b.SMTP_PORT as smtpPort,
		b.SMTP_LOGIN_SSl as smtpLoginSSL,
		b.SMTP_STARTTLS as smtpStarttls,
		b.POP3_PORT as pop3Port,
		b.POP3_LOGIN_SSL as pop3LoginSSL
	FROM
		t_send_email_account a
	LEFT JOIN
		t_send_email_conf b
	ON
		a.DOMAIN_NAME = b.DOMAIN_NAME
	WHERE
		a.`STATUS` = 1
"""

search_lock_domain_name = """
	SELECT 
		GROUP_CONCAT(t1.DOMAIN_NAME) as domainName 
	FROM (
		SELECT 
			DISTINCT t1.DOMAIN_NAME 
		FROM 
			t_send_email_account t1 
		WHERE 
			t1.status IN(0,2,3,4)  
		GROUP BY 
			DOMAIN_NAME
		) t1
"""

search_lock_user_name = """
	SELECT 
		COUNT(t1.ACCOUNT_ID) as num
	FROM 
		t_send_email_account t1 
	WHERE 
		t1.status IN(0,2,3,4)
	AND
		t1.USER_NAME = %s
	HAVING 
		num > 0 
"""





search_pop = """
	SELECT
		a.USER_NAME as userName,
		a.USER_PASSWORD as userPassword,
		b.POP3_SERVER as pop3Server,
		b.POP3_PORT as pop3Port,
		b.POP3_LOGIN_SSL as pop3LoginSSL
	FROM
		t_send_email_account a
	LEFT JOIN
		t_send_email_conf b
	ON
		a.DOMAIN_NAME = b.DOMAIN_NAME
	WHERE
		a.`STATUS` in (1,3)
"""

search_pop_server_ip = """
	SELECT
		a.USER_NAME as userName,
		a.USER_PASSWORD as userPassword,
		b.POP3_SERVER as pop3Server,
		b.POP3_PORT as pop3Port,
		b.POP3_LOGIN_SSL as pop3LoginSSL
	FROM
		t_send_email_account a
	LEFT JOIN
		t_send_email_conf b
	ON
		a.DOMAIN_NAME = b.DOMAIN_NAME
	INNER JOIN 
		t_server_domian_rel c 
	ON 
		c.DOMAIN_NAME = b.DOMAIN_NAME
	AND
		c.SERVER_IP = %s
	AND
		c.`STATUS` = 1
	WHERE
		a.`STATUS` in (1,3)
"""



search_smtp = """
	SELECT
		a.DOMAIN_NAME as domainName,
		a.USER_NAME as userName,
		a.USER_PASSWORD as userPassword,
		b.SMTP_SERVER as smtpServer,
		b.SMTP_PORT as smtpPort,
		b.SMTP_LOGIN_SSl as smtpLoginSSL,
		b.SMTP_STARTTLS as smtpStarttls
	FROM
		t_send_email_account a
	LEFT JOIN
		t_send_email_conf b
	ON
		a.DOMAIN_NAME = b.DOMAIN_NAME
	WHERE
		a.`STATUS` = 1
"""

search_valid_account = """
	SELECT
		t1.domainName,
		t1.userName,
		t1.userPassword,
		t1.smtpServer,
		t1.smtpPort,
		t1.smtpLoginSSL,
		t1.smtpStarttls,
		t1.residue as residue
	from(
		SELECT
				a.DOMAIN_NAME as domainName,
				a.USER_NAME as userName,
				a.USER_PASSWORD as userPassword,
				b.SMTP_SERVER as smtpServer,
				b.SMTP_PORT as smtpPort,
				b.SMTP_LOGIN_SSl as smtpLoginSSL,
				b.SMTP_STARTTLS as smtpStarttls,
				IFNULL(c.SELECT_COUNT,0) as selectCount,
				(a.MAX_SEND_COUNT-IFNULL(c.SELECT_COUNT,0)) as residue
			FROM
				t_send_email_account a
			LEFT JOIN
				t_send_email_conf b
			ON
				a.DOMAIN_NAME = b.DOMAIN_NAME
			INNER JOIN
				t_server_domian_rel d
			ON
				d.DOMAIN_NAME = b.DOMAIN_NAME
			AND
				d.`STATUS`='1'
			AND
				d.SERVER_IP = %s
			LEFT JOIN
				t_used_of_count c
			ON
				c.USED_CONTENT = a.USER_NAME AND c.INTIME >= %s AND c.INTIME <= %s
			WHERE
				a.`STATUS` = 1
	) t1
	WHERE
		t1.residue > 0
"""

search_and_update_account = """
	SELECT 
		DISTINCT domainName 
	FROM (
		SELECT 
			t1.DOMAIN_NAME as domainName
		FROM 
			t_send_email_conf t1 
		INNER JOIN
			t_server_domian_rel t3
		ON
			t1.DOMAIN_NAME = t3.DOMAIN_NAME
		AND
			t3.`STATUS`='1'
		AND
			t3.SERVER_IP = %s
		INNER JOIN
			t_send_email_account t2
		ON
			t1.DOMAIN_NAME = t2.DOMAIN_NAME
		AND	
			t2.`STATUS` NOT IN (2)
		WHERE 
			t1.`STATUS`=1 
		AND 
			t1.DOMAIN_NAME NOT IN (
				SELECT 
					DISTINCT SUBSTRING_INDEX(t1.USED_CONTENT,'@',-1) AS DOMAIN_NAME  
				FROM 
					t_used_of_count t1 
				WHERE 
					t1.USED_TYPE=2 
				AND 
					t1.INTIME >= %s 
				AND 
					t1.INTIME <= %s
			)
		ORDER BY t1.INTIME ASC
	)	t1
"""

search_lock_account = """
	SELECT 
		DISTINCT t.domainName 
	FROM (
		SELECT 
			t2.domainName,
			t2.selectCount,
			t3.maxSendCount 
		from (
			SELECT 
				SUBSTRING_INDEX(t1.USED_CONTENT,'@',-1) AS domainName,
				SUM(t1.SELECT_COUNT) AS selectCount,
				t1.MODTIME as usedModtime
			FROM 
				t_used_of_count t1 
			WHERE 
				t1.USED_TYPE=2 
			AND 
				date(t1.INTIME) = %s 
			GROUP BY domainName,t1.MODTIME 
			ORDER BY t1.MODTIME ASC,selectCount ASC
		) t2
		INNER JOIN (
			SELECT 
				DOMAIN_NAME as domainName,
				SUM(t1.MAX_SEND_COUNT) as maxSendCount,
				t1.MODTIME as accountModtime
			FROM t_send_email_account t1
			WHERE t1.`STATUS` = 3
			GROUP BY domainName,t1.MODTIME
		) t3
		ON
		 t2.domainName = t3.domainName
		AND
			TIMESTAMPDIFF(HOUR, t3.accountModtime, now()) >= %s
		HAVING t2.selectCount < t3.maxSendCount
		ORDER BY t2.usedModtime
	) t
"""

search_lock_account_for_user_name = """
	SELECT 
		DISTINCT t.userName
	FROM (
		SELECT 
			t1.USER_NAME as userName,
			t1.MAX_SEND_COUNT as maxSendCount,
			IFNULL(t2.SELECT_COUNT,0) as selectCount,
			TIMESTAMPDIFF(HOUR, t1.MODTIME, now()) as interval_time
		FROM
		 t_send_email_account t1
		LEFT JOIN
		 t_used_of_count t2
		ON
			t1.USER_NAME = t2.USED_CONTENT
		AND
			t2.USED_TYPE = 2
		AND
			date(t2.MODTIME) = %s
		WHERE
			t1.`STATUS`= 3
		AND
			TIMESTAMPDIFF(HOUR, t1.MODTIME, now()) >= %s
		HAVING CAST(selectCount AS SIGNED) < CAST(t1.MAX_SEND_COUNT AS SIGNED)
		UNION ALL(
			SELECT 
				t1.USER_NAME,
				t1.MAX_SEND_COUNT as maxSendCount,
				IFNULL(t2.SELECT_COUNT,0) as selectCount,
				TIMESTAMPDIFF(HOUR, t1.MODTIME, now()) as interval_time
			FROM
			 t_send_email_account t1
			LEFT JOIN
			 t_used_of_count t2
			ON
				t1.USER_NAME = t2.USED_CONTENT
			AND
				t2.USED_TYPE = 2
			AND
				date(t2.MODTIME) = %s
			WHERE
				t1.`STATUS`= 4
			AND
				TIMESTAMPDIFF(HOUR, t1.MODTIME, now()) >= 24
			HAVING CAST(selectCount AS SIGNED) < CAST(t1.MAX_SEND_COUNT AS SIGNED)
		)
	) t
"""





update = """
	UPDATE t_send_email_account SET `STATUS` = %s,MODTIME = now() WHERE ACCOUNT_ID = '%s'
"""

update_status = """
	UPDATE 
		t_send_email_account 
	SET 
		`STATUS` = %s,
		MODTIME = now() 
	WHERE 
		`STATUS` = %s 
	AND 
		DOMAIN_NAME IN (
			SELECT 
				DOMAIN_NAME 
			FROM 
				t_server_domian_rel t1 
			WHERE 
				t1.SERVER_IP = %s
			)
"""

update_all_status_valid = """
	UPDATE 
		t_send_email_account 
	SET 
		`STATUS` = 1,
		MODTIME = now() 
	WHERE 
		`STATUS` in(3)
"""


update_domain_name = """
	UPDATE t_send_email_account SET `STATUS` = %s,MODTIME = now() WHERE `DOMAIN_NAME` = %s
"""

update_user_name = """
	UPDATE t_send_email_account SET `STATUS` = %s,MODTIME = now() WHERE `USER_NAME` = %s
"""

