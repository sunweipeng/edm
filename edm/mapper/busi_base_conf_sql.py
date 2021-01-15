search = """
	SELECT 
		t.BUSI_KEY as busiKey,
		t.BUSI_VALUE as busiValue,
		t.`STATUS` as status
	FROM
		t_busi_base_conf t
	WHERE
		t.`STATUS` = 1
"""

search_by_key = """
	SELECT 
		t.BUSI_KEY as busiKey,
		t.BUSI_VALUE as busiValue,
		t.`STATUS` as status
	FROM
		t_busi_base_conf t
	WHERE
		t.`STATUS` = 1
	AND 
		t.BUSI_KEY = %s
"""