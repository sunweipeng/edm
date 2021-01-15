search_task_code_by_server_ip = """
	SELECT 
		t1.REL_ID as relId,
		t1.CHANNEL_CODE as channelCode,
		t2.TASK_CODE as taskCode,
		t3.TASK_TYPE as taskType
	FROM 
		t_channel_server_rel t1 
	LEFT JOIN
	  t_task_channel_rel t2
	ON
		t1.CHANNEL_CODE = t2.CHANNEL_CODE
	AND
		t1.`STATUS`=t2.`STATUS`
	INNER JOIN
		t_task t3
	ON
		t2.TASK_CODE = t3.TASK_CODE and t3.`STATUS`=2
	WHERE 
		t1.SERVER_IP= %s
	AND
	  t1.`STATUS`=1
	ORDER BY
	  t3.MODTIME ASC
	LIMIT 0,1
"""

