#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.observer import Observer
from util.queue_manager_helper import QueueManagerHelper
from service.server_conf_service import ServerConfService
from config import busi_config

class QueueManagerObserver(Observer):
    """
    处理相关队列
    """
    def update(self):
        pass

    def search_server_ip(self):
        """
        查询服务器Ip地址，生成方法名
        :return:
        """
        server_list = ServerConfService().search()
        if not server_list:
            return []
        register_list = ["get_result_queue"]
        [register_list.append("get_%s_queue" % item.get("serverIp").replace(".", "_")) for item in server_list]
        return register_list

    def queue_manager_helper(self):
        """
        处理队列
        :return:
        """
        manager = None
        try:
            regisger_name = self.search_server_ip()
            if not regisger_name:
                return False
            manager = QueueManagerHelper('', busi_config.QUEUE_MANAGER_AUTH_KEY, regisger_name)
            manager.master_start()

            task_106_12_219_104_queue = eval("manager.server.get_106_12_219_104_queue")()
            result = manager.server.get_result_queue()

            # 添加任务
            for url in ["ImageUrl_" + str(i) for i in range(10)]:
                print('url is %s' % url)
                task_106_12_219_104_queue.put(url)
            print('try get result')
            for i in range(10):
                print('result is %s' % result.get(timeout=10))
        except Exception as e:
            self.logger.error("【任务队列】创建任务队列异常，异常信息为：%s" % traceback.format_exc())
        finally:
            """判断是否为空"""
            if manager:
                manager.queue_close()



