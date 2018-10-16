#!/usr/bin/python
# -*- coding: UTF-8 -*-'
import logging
import logging.config
import time
from selenium import webdriver
import configparser
import redis

CSDN_NET_ = "https://me.csdn.net/"

Config = configparser.ConfigParser()
Config.read("config.ini")
logfilePath = Config.get("logfile", "path")
# 读取日志配置文件内容
logging.config.fileConfig(logfilePath)

# 创建一个日志器logger
logger = logging.getLogger('app')

redis_conn = redis.Redis(host='192.168.0.1', port=6379, password='xueyou123')
KEY_IDS = 'csdn_ids'
KEY_USER_INFO = 'csdn_id_info'

user_list = []


def open_driver():
    global driver
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chromedriverPath = Config.get("chromedriver", "path")
    print(chromedriverPath)
    driver = webdriver.Chrome(executable_path=chromedriverPath, options=chrome_options)


def real_craw(user_id):
    # 重新开一个窗口进行截图
    exe_js_str = 'window.open("");'
    driver.execute_script(exe_js_str)
    allHandles = driver.window_handles
    driver.switch_to.window(allHandles[1])
    driver.get('%s%s' % (csdn_net_prefix, user_id))
    guanzhu_ele = driver.find_elements_by_class_name('fans_title')
    if guanzhu_ele is not None:
        for ele in guanzhu_ele:
            nickname = ele.text
            id = ele.get_attribute('href')[20:]
            user_list.append(id)
            if redis_conn.sismember(KEY_IDS, id) == 0:
                logger.info('%s:%s' % (id, nickname))
                redis_conn.sadd(KEY_IDS, id)
                redis_conn.hset('%s%s' % (KEY_USER_INFO, id), 'nickname', nickname)
    driver.close()
    driver.switch_to.window(allHandles[0])


if __name__ == '__main__':
    logger.debug('debug')
    logger.info('info')
    logger.warn('warn')
    logger.error('error')
    print('test over...')
    try:
        open_driver()
        csdn_net_prefix = CSDN_NET_

        real_craw('love__coder')
        print(user_list)
        while len(user_list) < 200:
            print('now lenth is :%s' % len(user_list))
            for user in user_list:
                print('handle user:%s' % user)
                real_craw(user)
        time.sleep(500)
    finally:
        driver.close()
