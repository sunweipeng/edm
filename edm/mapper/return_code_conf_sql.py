search = """
	SELECT 
		t.CONF_ID as confId,
		t.RET_CODE as retCode,
		t.RET_MSG as retMsg,
		t.`STATUS` as status,
		t.POLICY as policy,
		t.INTIME as intime,
		t.MODTIME as modtime
	FROM
		t_return_code_conf t
	WHERE
		t.`STATUS` = 1
"""

search_by_ret_code = """
	SELECT 
		t.CONF_ID as confId,
		t.RET_CODE as retCode,
		t.RET_MSG as retMsg,
		t.`STATUS` as status,
		t.POLICY as policy,
		t.INTIME as intime,
		t.MODTIME as modtime
	FROM
		t_return_code_conf t
	WHERE
		t.`STATUS` = 1
	AND 
		t.RET_CODE = '%s'
"""
