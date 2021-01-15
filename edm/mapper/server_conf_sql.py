search = """
	SELECT
		a.SERVER_ID as serverId,
		a.SERVER_IP as serverIp,
		a.IS_NEED_PROXY as isNeedProxy
	FROM 
		t_server_conf a
	WHERE
		a.`STATUS` = 1
"""

update = """
	UPDATE t_server_conf SET `STATUS` = %s,MODTIME = now() WHERE SERVER_ID = %s
"""