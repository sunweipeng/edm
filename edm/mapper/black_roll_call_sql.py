insert = """
	INSERT INTO `t_black_white_roll_call`(`CONTENT`,`CONTENT_TYPE`,`ROLL_CALL_TYPE`,`STATUS`,`INTIME`,`MODTIME`) VALUES ('%s', '%s', '%s', '%s', now(),now())
"""

search = """
	SELECT 
		t.ROLL_CALL_ID as rollCallId,
		t.CONTENT as content,
		t.CONTENT_TYPE as contentType,
		t.ROLL_CALL_TYPE as rollCallType,
		t.`STATUS` as status
	FROM
		t_black_white_roll_call t
	WHERE
		t.`STATUS` = 1
	AND
		t.CONTENT_TYPE = %s
	AND
	  t.ROLL_CALL_TYPE = %s
"""

search_key = """
	SELECT
        t1.content
    FROM
     (
        SELECT
            t1.CONTENT as content
        FROM
            t_black_roll_call t1
        WHERE
            t1.`STATUS`= 1
        AND
            t1.CONTENT_TYPE = 0
     UNION ALL
         SELECT 
            DISTINCT t2.FEEDBACK_ACCOUNT as content
         FROM
            t_account_feedback t2
         WHERE
            t2.`STATUS`= 1
     ) t1  
"""
