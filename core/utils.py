'''
Author: 邹洋
Date: 2021-08-14 09:56:23
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-14 10:00:51
Description: 工具类
'''
import time

def time_start():
    return time.time()

def time_end(t,str='耗时'):
    print(f'{str}:{time.time() - t:.8f}s')