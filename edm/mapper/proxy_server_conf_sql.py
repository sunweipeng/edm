search = """
	SELECT 
		t.PROXY_SERVER_ID as proxyServerId,
		t.PROXY_SERVER_IP as proxyServerIp,
		t.PROXY_SERVER_PORT as proxyServerPort,
		t.PROXY_TYPE as proxyType,
		t.USER_NAME as userName,
		t.USER_PASSWORD as userPassword,
		t.`STATUS` as status
	FROM
		t_proxy_server_conf t
	WHERE
		t.`STATUS` = 1
	AND 
		t.PROXY_TYPE = %s
"""

update = """
	UPDATE t_proxy_server_conf SET `STATUS` = %s, MODTIME = now() WHERE PROXY_SERVER_ID = '%s'
"""

