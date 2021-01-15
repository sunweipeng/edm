search = """
	SELECT 
		t1.TEMPLATE_CODE as templateCode,
		t1.TEMPLATE_PATH as templatePath,
		t3.TEMPLATE_EXT_CODE as templateExtCode,
		t3.TEMPLATE_SUBJECT as templateSubject,
		t3.TEMPLATE_FROM as templateFrom,
		t3.TEMPLATE_CONTENT as templateContent,
		t3.TEMPLATE_TO as templateTo
	FROM
		t_template t1
	INNER JOIN
		t_template_ext_rel t2
	ON
		t1.TEMPLATE_CODE = t2.TEMPLATE_CODE
	AND
		t1.`STATUS` = t2.`STATUS`
	INNER JOIN
		t_template_ext t3
	ON
		t2.TEMPLATE_EXT_CODE = t3.TEMPLATE_EXT_CODE
	AND
		t2.`STATUS` = t3.`STATUS`
	WHERE
		t1.TEMPLATE_CODE = %s
	AND
		t1.`STATUS`=1
"""

search_template_code = """
	SELECT 
		t1.TEMPLATE_CODE as templateCode
	FROM
	  t_task_template_rel t1
	WHERE
		t1.TASK_CODE = %s
	AND
		t1.`STATUS`=1
"""