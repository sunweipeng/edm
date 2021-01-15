insert = """
	INSERT INTO `t_email_address_book`(`MOBILE`,`EMAIL`,`STATUS`,`INTIME`,`MODTIME`) VALUES ('%s', '%s', '%s', now(),now())
"""

search = """
	SELECT 
		t.BOOK_ID as bookId,
		t.MOBILE as mobile,
		t.EMAIL as email,
		t.`STATUS` as status,
		t.INTIME as intime,
		t.MODTIME as modtime
	FROM
		t_email_address_book t
	WHERE
		t.`STATUS` = %s
"""

update = """
	UPDATE t_email_address_book SET `STATUS` = %s,MODTIME = now() WHERE BOOK_ID = '%s'
"""