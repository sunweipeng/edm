

/*Table structure for table `t_account_feedback` */

DROP TABLE IF EXISTS `t_account_feedback`;

CREATE TABLE `t_account_feedback` (
  `FEEDBACK_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `FEEDBACK_ACCOUNT` varchar(64) NOT NULL,
  `FEEDBACK_TYPE` smallint(6) NOT NULL,
  `FEEDBACK_REASON` varchar(512) DEFAULT NULL,
  `STATUS` smallint(6) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`FEEDBACK_ID`),
  KEY `FEEDBACK_ACCOUNT` (`FEEDBACK_ACCOUNT`) USING BTREE,
  KEY `FEEDBACK_TYPE` (`FEEDBACK_TYPE`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Table structure for table `t_black_roll_call` */

DROP TABLE IF EXISTS `t_black_roll_call`;

CREATE TABLE `t_black_roll_call` (
  `ROLL_CALL_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CONTENT` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `CONTENT_TYPE` smallint(6) NOT NULL DEFAULT '-99',
  `STATUS` smallint(6) NOT NULL DEFAULT '-99',
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`ROLL_CALL_ID`),
  KEY `CONTENT` (`CONTENT`) USING BTREE,
  KEY `CONTENT_TYPE` (`CONTENT_TYPE`) USING BTREE,
  KEY `STATUS` (`STATUS`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1810 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_busi_base_conf` */

DROP TABLE IF EXISTS `t_busi_base_conf`;

CREATE TABLE `t_busi_base_conf` (
  `CONF_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `BUSI_KEY` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `BUSI_VALUE` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `STATUS` smallint(6) NOT NULL DEFAULT '-99',
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`CONF_ID`),
  KEY `BUSI_KEY` (`BUSI_KEY`) USING BTREE,
  KEY `BUSI_VALUE` (`BUSI_VALUE`(191)) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_channel_server_rel` */

DROP TABLE IF EXISTS `t_channel_server_rel`;

CREATE TABLE `t_channel_server_rel` (
  `REL_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CHANNEL_CODE` varchar(32) NOT NULL,
  `SERVER_IP` varchar(32) NOT NULL,
  `STATUS` smallint(1) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`REL_ID`),
  KEY `CHANNEL_CODE` (`CHANNEL_CODE`) USING BTREE,
  KEY `SERVER_IP` (`SERVER_IP`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Table structure for table `t_email_address_book` */

DROP TABLE IF EXISTS `t_email_address_book`;

CREATE TABLE `t_email_address_book` (
  `BOOK_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `MOBILE` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `EMAIL` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `STATUS` smallint(6) NOT NULL DEFAULT '-99' COMMENT '状态码',
  `INTIME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '入库时间',
  `MODTIME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`BOOK_ID`),
  UNIQUE KEY `MOBILE` (`MOBILE`,`EMAIL`) USING BTREE,
  KEY `STATUS` (`STATUS`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_file_read_record` */

DROP TABLE IF EXISTS `t_file_read_record`;

CREATE TABLE `t_file_read_record` (
  `RECORD_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `TASK_CODE` varchar(32) NOT NULL,
  `FILE_NAME` varchar(128) NOT NULL,
  `READ_OFFSET` varchar(32) NOT NULL,
  `READ_LINES` varchar(32) NOT NULL,
  `STATUS` smallint(6) NOT NULL DEFAULT '0',
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`RECORD_ID`),
  KEY `TASK_CODE` (`TASK_CODE`) USING BTREE,
  KEY `FILE_NAME` (`FILE_NAME`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Table structure for table `t_marketing_data` */

DROP TABLE IF EXISTS `t_marketing_data`;

CREATE TABLE `t_marketing_data` (
  `MARKETING_DATA_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `ORIGINAL_BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '原始批次号',
  `SUB_BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '子批次号',
  `MOBILE` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `EMAIL` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `SEND_COUNT` varchar(9) COLLATE utf8mb4_unicode_ci DEFAULT '1' COMMENT '投递次数',
  `SEND_RESULT` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '投递结果',
  `STATUS` smallint(6) NOT NULL DEFAULT '-99' COMMENT '状态码',
  `INTIME` datetime NOT NULL COMMENT '入库时间',
  `MODTIME` datetime NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`MARKETING_DATA_ID`),
  KEY `BATCH_CODE` (`BATCH_CODE`) USING BTREE,
  KEY `SUB_BATCH_CODE` (`SUB_BATCH_CODE`) USING BTREE,
  KEY `MOBILE` (`MOBILE`) USING BTREE,
  KEY `EMAIL` (`EMAIL`) USING BTREE,
  KEY `STATUS` (`STATUS`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=16162 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_marketing_data_bak` */

DROP TABLE IF EXISTS `t_marketing_data_bak`;

CREATE TABLE `t_marketing_data_bak` (
  `MARKETING_DATA_ID` bigint(20) unsigned zerofill NOT NULL DEFAULT '00000000000000000000' COMMENT '主键ID',
  `BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '原始批次号',
  `SUB_BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '子批次号',
  `MOBILE` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号',
  `EMAIL` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `SEND_COUNT` varchar(9) COLLATE utf8mb4_unicode_ci DEFAULT '1' COMMENT '投递次数',
  `SEND_RESULT` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '投递结果',
  `STATUS` smallint(6) DEFAULT '-99' COMMENT '状态码',
  `INTIME` datetime NOT NULL COMMENT '入库时间',
  `MODTIME` datetime NOT NULL COMMENT '修改时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_pop_record` */

DROP TABLE IF EXISTS `t_pop_record`;

CREATE TABLE `t_pop_record` (
  `RECORD_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `SUB_BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `MOBILE` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `EMAIL` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `SEND_ACCOUNT` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `POP3_ACCOUNT` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SEND_SUBJECT` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SEND_RESULT` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `RESULT_TEXT` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `RESULT_HTML` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `RESULT_ATTACH` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `STATUS` smallint(6) NOT NULL DEFAULT '-99',
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`RECORD_ID`),
  KEY `BATCH_CODE` (`BATCH_CODE`) USING BTREE,
  KEY `MOBILE` (`MOBILE`) USING BTREE,
  KEY `EMAIL` (`EMAIL`) USING BTREE,
  KEY `STATUS` (`STATUS`) USING BTREE,
  KEY `SUB_BATCH_CODE` (`SUB_BATCH_CODE`) USING BTREE,
  KEY `POP3_ACCOUNT` (`POP3_ACCOUNT`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7038 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_primary_data` */

DROP TABLE IF EXISTS `t_primary_data`;

CREATE TABLE `t_primary_data` (
  `PRIMARY_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `ORIGINAL_BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `MOBILE` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `EMAIL` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `STATUS` smallint(6) NOT NULL DEFAULT '-99',
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`PRIMARY_ID`),
  KEY `MOBILE` (`MOBILE`) USING BTREE,
  KEY `BATCH_CODE` (`BATCH_CODE`) USING BTREE,
  KEY `EMAIL` (`EMAIL`) USING BTREE,
  KEY `STATUS` (`STATUS`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=977686 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_proxy_server_conf` */

DROP TABLE IF EXISTS `t_proxy_server_conf`;

CREATE TABLE `t_proxy_server_conf` (
  `PROXY_SERVER_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `PROXY_SERVER_IP` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务器IP地址',
  `PROXY_SERVER_PORT` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务器端口',
  `PROXY_TYPE` smallint(6) NOT NULL DEFAULT '-99' COMMENT '代理类型',
  `USER_NAME` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '登录账号',
  `USER_PASSWORD` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '登录密码',
  `WEIGHT` smallint(6) NOT NULL,
  `STATUS` smallint(6) NOT NULL DEFAULT '-99' COMMENT '状态码',
  `INTIME` datetime NOT NULL COMMENT '入库时间',
  `MODTIME` datetime NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`PROXY_SERVER_ID`),
  KEY `PROXY_SERVER_IP` (`PROXY_SERVER_IP`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_send_channel` */

DROP TABLE IF EXISTS `t_send_channel`;

CREATE TABLE `t_send_channel` (
  `CHANNEL_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `CHANNEL_CODE` varchar(32) NOT NULL,
  `CHANNEL_NAME` varchar(64) NOT NULL,
  `CHANNEL_DESCRIBE` varchar(256) NOT NULL,
  `STATUS` smallint(1) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`CHANNEL_ID`),
  KEY `CHANNEL_CODE` (`CHANNEL_CODE`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Table structure for table `t_send_email_account` */

DROP TABLE IF EXISTS `t_send_email_account`;

CREATE TABLE `t_send_email_account` (
  `ACCOUNT_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `DOMAIN_NAME` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '域名',
  `USER_NAME` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '登录名',
  `USER_PASSWORD` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '登录密码',
  `MAX_SEND_COUNT` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '每天最大发送量',
  `WEIGHT` smallint(6) NOT NULL,
  `STATUS` smallint(6) NOT NULL DEFAULT '-99' COMMENT '状态码',
  `INTIME` datetime NOT NULL COMMENT '入库时间',
  `MODTIME` datetime NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`ACCOUNT_ID`),
  KEY `DOMAIN_NAME` (`DOMAIN_NAME`) USING BTREE,
  KEY `USER_NAME` (`USER_NAME`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_send_email_conf` */

DROP TABLE IF EXISTS `t_send_email_conf`;

CREATE TABLE `t_send_email_conf` (
  `CONF_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `DOMAIN_NAME` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '域名',
  `SMTP_SERVER` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'smtp服务器地址',
  `POP3_SERVER` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'pop3服务器地址',
  `SMTP_PORT` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'smtp端口',
  `SMTP_LOGIN_SSl` smallint(6) NOT NULL DEFAULT '-99' COMMENT 'smtp是否加密登录',
  `SMTP_STARTTLS` smallint(6) NOT NULL DEFAULT '-99' COMMENT 'smtp是否加密传输',
  `POP3_PORT` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'pop3端口',
  `POP3_LOGIN_SSL` smallint(6) NOT NULL DEFAULT '-99' COMMENT 'pop3是否加密登录',
  `STATUS` smallint(6) NOT NULL DEFAULT '-99' COMMENT '状态码',
  `INTIME` datetime NOT NULL COMMENT '入库时间',
  `MODTIME` datetime NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`CONF_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_send_record` */

DROP TABLE IF EXISTS `t_send_record`;

CREATE TABLE `t_send_record` (
  `RECORD_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `SUB_BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `BATCH_CODE` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `MOBILE` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `TEMPLATE_EXT_CODE` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `EMAIL` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SERVER_IP` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SEND_ACCOUNT` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `STATUS` smallint(6) NOT NULL DEFAULT '-99',
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`RECORD_ID`),
  KEY `BATCH_CODE` (`BATCH_CODE`) USING BTREE,
  KEY `MOBILE` (`MOBILE`) USING BTREE,
  KEY `EMAIL` (`EMAIL`) USING BTREE,
  KEY `TEMPLATE_EXT_CODE` (`TEMPLATE_EXT_CODE`) USING BTREE,
  KEY `SERVER_IP` (`SERVER_IP`) USING BTREE,
  KEY `SEND_ACCOUNT` (`SEND_ACCOUNT`) USING BTREE,
  KEY `STATUS` (`STATUS`) USING BTREE,
  KEY `SUB_BATCH_CODE` (`SUB_BATCH_CODE`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=22343 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_server_conf` */

DROP TABLE IF EXISTS `t_server_conf`;

CREATE TABLE `t_server_conf` (
  `SERVER_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `SERVER_IP` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务器IP地址',
  `SERVER_VENDOR` smallint(6) NOT NULL DEFAULT '-99' COMMENT '服务器厂商',
  `USER_NAME` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号',
  `USER_PASSWORD` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `IS_NEED_PROXY` smallint(6) NOT NULL COMMENT '是否需要代理',
  `WEIGHT` smallint(6) NOT NULL,
  `STATUS` smallint(6) NOT NULL DEFAULT '-99' COMMENT '状态码',
  `INTIME` datetime NOT NULL COMMENT '入库时间',
  `MODTIME` datetime NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`SERVER_ID`),
  KEY `SERVER_IP` (`SERVER_IP`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_server_domian_rel` */

DROP TABLE IF EXISTS `t_server_domian_rel`;

CREATE TABLE `t_server_domian_rel` (
  `REL_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `SERVER_IP` varchar(32) NOT NULL,
  `DOMAIN_NAME` varchar(64) NOT NULL,
  `STATUS` smallint(1) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`REL_ID`),
  KEY `SERVER_IP` (`SERVER_IP`) USING BTREE,
  KEY `DOMAIN_NAME` (`DOMAIN_NAME`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

/*Table structure for table `t_support_verify_email` */

DROP TABLE IF EXISTS `t_support_verify_email`;

CREATE TABLE `t_support_verify_email` (
  `VERIFY_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `DOMAIN_NAME` varchar(64) NOT NULL,
  `VERIFY_TYPE` smallint(1) NOT NULL COMMENT '1 RCPT 2 注册验证',
  `STATUS` smallint(1) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`VERIFY_ID`),
  KEY `DOMAIN_NAME` (`DOMAIN_NAME`) USING BTREE,
  KEY `VERIFY_TYPE` (`VERIFY_TYPE`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `t_task` */

DROP TABLE IF EXISTS `t_task`;

CREATE TABLE `t_task` (
  `TASK_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `TASK_CODE` varchar(32) NOT NULL,
  `TASK_NAME` varchar(64) NOT NULL,
  `TASK_DESCRIBE` varchar(256) NOT NULL,
  `TASK_TYPE` smallint(6) NOT NULL DEFAULT '1',
  `STATUS` smallint(1) NOT NULL COMMENT '0 禁用  1 待发送 2 发送中 3 发送成功 4 发送终止 ',
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`TASK_ID`),
  KEY `TASK_CODE` (`TASK_CODE`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Table structure for table `t_task_channel_rel` */

DROP TABLE IF EXISTS `t_task_channel_rel`;

CREATE TABLE `t_task_channel_rel` (
  `REL_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `TASK_CODE` varchar(32) NOT NULL,
  `CHANNEL_CODE` varchar(32) NOT NULL,
  `STATUS` smallint(6) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`REL_ID`),
  KEY `TASK_CODE` (`TASK_CODE`) USING BTREE,
  KEY `CHANNEL_CODE` (`CHANNEL_CODE`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Table structure for table `t_task_template_rel` */

DROP TABLE IF EXISTS `t_task_template_rel`;

CREATE TABLE `t_task_template_rel` (
  `REL_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `TASK_CODE` varchar(32) NOT NULL,
  `TEMPLATE_CODE` varchar(32) NOT NULL,
  `STATUS` smallint(1) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`REL_ID`),
  KEY `TASK_CODE` (`TASK_CODE`) USING BTREE,
  KEY `TEMPLATE_CODE` (`TEMPLATE_CODE`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Table structure for table `t_template` */

DROP TABLE IF EXISTS `t_template`;

CREATE TABLE `t_template` (
  `TEMPLATE_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `TEMPLATE_CODE` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板编码',
  `TEMPLATE_NAME` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板名称',
  `TEMPLATE_PATH` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板路径',
  `STATUS` smallint(6) NOT NULL DEFAULT '-99' COMMENT '状态码',
  `INTIME` datetime NOT NULL COMMENT '入库时间',
  `MODTIME` datetime NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`TEMPLATE_ID`),
  KEY `TEMPLATE_CODE` (`TEMPLATE_CODE`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_template_ext` */

DROP TABLE IF EXISTS `t_template_ext`;

CREATE TABLE `t_template_ext` (
  `TEMPLATE_EXT_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `TEMPLATE_EXT_CODE` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '扩展编码',
  `TEMPLATE_SUBJECT` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板标题',
  `TEMPLATE_CONTENT` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板内容',
  `TEMPLATE_FROM` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发件人',
  `TEMPLATE_TO` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收件人',
  `STATUS` smallint(6) NOT NULL DEFAULT '-99' COMMENT '状态码',
  `INTIME` datetime NOT NULL COMMENT '入库时间',
  `MODTIME` datetime NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`TEMPLATE_EXT_ID`),
  KEY `TEMPLATE_EXT_CODE` (`TEMPLATE_EXT_CODE`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Table structure for table `t_template_ext_rel` */

DROP TABLE IF EXISTS `t_template_ext_rel`;

CREATE TABLE `t_template_ext_rel` (
  `REL_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `TEMPLATE_CODE` varchar(32) NOT NULL,
  `TEMPLATE_EXT_CODE` varchar(32) NOT NULL,
  `STATUS` smallint(1) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`REL_ID`),
  KEY `TEMPLATE_CODE` (`TEMPLATE_CODE`) USING BTREE,
  KEY `TEMPLATE_EXT_CODE` (`TEMPLATE_EXT_CODE`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;

/*Table structure for table `t_used_of_count` */

DROP TABLE IF EXISTS `t_used_of_count`;

CREATE TABLE `t_used_of_count` (
  `USED_OF_ID` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `USED_CONTENT` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号内容',
  `USED_TYPE` smallint(6) NOT NULL DEFAULT '-99' COMMENT '1:服务器 2：发送账号 3：发送模板',
  `USED_COUNT` varchar(9) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0',
  `SELECT_COUNT` varchar(9) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0',
  `STATUS` smallint(6) NOT NULL,
  `INTIME` datetime NOT NULL,
  `MODTIME` datetime NOT NULL,
  PRIMARY KEY (`USED_OF_ID`),
  KEY `USED_CONTENT` (`USED_CONTENT`) USING BTREE,
  KEY `USED_TYPE` (`USED_TYPE`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2442 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;