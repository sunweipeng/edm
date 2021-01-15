-- 新增营销数据
-- select date(t1.INTIME),count(t1.MARKETING_DATA_ID) from t_marketing_data t1 where date(t1.INTIME) = date(t1.MODTIME) GROUP BY date(t1.INTIME)

-- 发送总数
-- select date(t1.MODTIME),count(t1.MARKETING_DATA_ID) from t_marketing_data t1 GROUP BY date(t1.MODTIME)
-- 发送成功数
-- select date(t.INTIME),count(t.MARKETING_DATA_ID) from t_marketing_data t where t.`STATUS`in (1,3) and date(t.INTIME) = date(t.MODTIME) GROUP BY date(t.INTIME)


-- 发送失败数
-- select date(t.INTIME),count(t.MARKETING_DATA_ID) from t_marketing_data t where t.`STATUS` not in (1,3) and date(t.INTIME) = date(t.MODTIME) GROUP BY date(t.INTIME)

-- 重复营销
-- select date(t1.MODTIME),count(t1.MARKETING_DATA_ID) from t_marketing_data t1 WHERE date(t1.INTIME) != date(t1.MODTIME) GROUP BY date(t1.MODTIME)

-- 查询账号选择量
-- select SUBSTRING_INDEX(t1.USED_CONTENT,'@',-1) as domainName,SUM(t1.SELECT_COUNT) as SELECT_COUNT from t_used_of_count t1 WHERE date(t1.INTIME) = '2019-05-10' and t1.USED_TYPE='2' GROUP BY domainName
-- 查询账号使用量
-- select SUBSTRING_INDEX(t1.USED_CONTENT,'@',-1) as domainName,SUM(t1.USED_COUNT) as SELECT_COUNT from t_used_of_count t1 WHERE date(t1.INTIME) = '2019-05-10' and t1.USED_TYPE='2' GROUP BY domainName
-- 按域名统计使用量
-- select date(t1.INTIME),SUBSTRING_INDEX(t1.USED_CONTENT,'@',-1) as domainName,SUM(t1.USED_COUNT) as SELECT_COUNT from t_used_of_count t1 WHERE date(t1.INTIME) = '2019-05-10' and t1.USED_TYPE='2' GROUP BY date(t1.INTIME),domainName
-- 按天统计使用量
-- select date(t1.INTIME),SUM(t1.USED_COUNT) as SELECT_COUNT from t_used_of_count t1 WHERE date(t1.INTIME) = '2019-05-10' and t1.USED_TYPE='2' GROUP BY date(t1.INTIME)
-- select date(t1.INTIME) ,SUM(t1.USED_COUNT) as SELECT_COUNT from t_used_of_count t1 WHERE t1.USED_TYPE='2' GROUP BY date(t1.INTIME)

-- select SUM(t1.SELECT_COUNT) as SELECT_COUNT from t_used_of_count t1 WHERE date(t1.INTIME) = '2019-05-09' and t1.USED_TYPE='2'

-- 
-- INSERT INTO `t_send_email_conf`(`DOMAIN_NAME`,`SMTP_SERVER`,`POP3_SERVER`,`SMTP_PORT`,`SMTP_LOGIN_SSl`,`SMTP_STARTTLS`,`POP3_PORT`,`POP3_LOGIN_SSL`,`STATUS`,`INTIME`,`MODTIME`) SELECT DISTINCT t1.DOMAIN_NAME,CONCAT('smtp.',t1.DOMAIN_NAME), CONCAT('pop3.',t1.DOMAIN_NAME),'25', '0', '0', '110', '0', '1',now(),now() from t_send_email_account t1 WHERE t1.DOMAIN_NAME not in('cnhelper.com','i9bee.com','m7bee.cn','x7bee.cn')

-- update t_send_email_account t1 set t1.`STATUS`='3' WHERE t1.DOMAIN_NAME='i9bee.com'

-- update t_send_email_account t1 set t1.`STATUS`='1' WHERE t1.DOMAIN_NAME='aoyousky0316.com'

-- UPDATE t_send_email_account t1 set t1.USER_NAME='xianlin_090508_7@aoyousky0316.com' WHERE t1.USER_NAME='xianlin_090508_7@aoyousky0316.co'

-- update t_send_email_account t1 set t1.`STATUS`=1 WHERE t1.DOMAIN_NAME='ruiwowo.cn' 
-- UPDATE t_send_email_account t1 set t1.`STATUS`=1 where t1.`STATUS`=3

-- SELECT * from t_send_record t1 where t1.`STATUS` not in (0,1)
-- SELECT SUBSTRING_INDEX(t1.USER_NAME,'@',1) as domainName from t_send_email_account t1 where t1.DOMAIN_NAME='ruiwowo.com'

-- UPDATE t_send_email_account t1 set t1.DOMAIN_NAME='ruiwowo.cn',t1.USER_NAME=CONCAT(SUBSTRING_INDEX(t1.USER_NAME,'@',1),'@ruiwowo.cn') where t1.DOMAIN_NAME='ruiwowo.com'