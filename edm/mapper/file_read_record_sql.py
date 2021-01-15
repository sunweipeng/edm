insert = """
	INSERT INTO `t_file_read_record`(`TASK_CODE`,`FILE_NAME`,`READ_OFFSET`,`READ_LINES`,`STATUS`,`INTIME`,`MODTIME`) VALUES (%s, %s, %s, %s, %s,now(),now())
"""

update = """
	UPDATE t_file_read_record t1 SET t1.READ_OFFSET=%s,t1.READ_LINES=t1.READ_LINES+%s,t1.`STATUS`=%s,t1.MODTIME=now() WHERE t1.TASK_CODE=%s AND t1.FILE_NAME=%s
"""

search = """
	SELECT 
		t1.TASK_CODE As taskCode,
		t1.FILE_NAME AS fileName,
		t1.READ_OFFSET AS readOffset,
		t1.READ_LINES AS readLines,
		t1.`STATUS` AS status 
	FROM 
		t_file_read_record t1 
	WHERE 
		t1.TASK_CODE = %s 
	AND 
		t1.`STATUS`=%s
	ORDER BY
		t1.MODTIME DESC
"""

