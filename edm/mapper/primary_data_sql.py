search = """
	SELECT 		
		t.MOBILE as mobile,
		t.BATCH_CODE as batchCode,
		t.ORIGINAL_BATCH_CODE as originalBatchCode,
		t.EMAIL as email		
	FROM
		t_primary_data t
	WHERE
		t.`STATUS` = 1
	AND 
		t.BATCH_CODE = %s
"""

update = """
	UPDATE t_primary_data SET BATCH_CODE = %s,`STATUS`= 1, MODTIME = now() WHERE `STATUS` = 0 AND ORIGINAL_BATCH_CODE = %s LIMIT %s
"""

update_roll_back = """
	UPDATE t_primary_data SET BATCH_CODE = NULL,`STATUS`= 0, MODTIME = now() WHERE `BATCH_CODE` = %s AND ORIGINAL_BATCH_CODE = %s
"""
