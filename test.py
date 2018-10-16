#!/usr/bin/python
# -*- coding: UTF-8 -*-'
import redis
redis_conn = redis.Redis(host='www.wuxueyou.cn', port=6379, password='xueyou123')
KEY_IDS = 'csdn_ids'
KEY_USER_INFO = 'csdn_id_info'
if __name__ == '__main__':
    num = redis_conn.scard(KEY_IDS)
    print(num)
