#!/usr/bin/python
# -*- coding: UTF-8 -*-'
import logging
import logging.config
import time
from selenium import webdriver
import configparser

Config = configparser.ConfigParser()
Config.read("config.ini")
logfilePath = Config.get("logfile", "path")
# 读取日志配置文件内容
logging.config.fileConfig(logfilePath)

# 创建一个日志器logger
logger = logging.getLogger('app')

if __name__ == '__main__':
    logger.debug('debug')
    logger.info('info')
    logger.warn('warn')
    logger.error('error')
    print('test over...')
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chromedriverPath = Config.get("chromedriver", "path")
    print(chromedriverPath)
    driver = webdriver.Chrome(executable_path=chromedriverPath, options=chrome_options)
    driver.get("http://www.baidu.com")
    time.sleep(10)
    driver.close()

