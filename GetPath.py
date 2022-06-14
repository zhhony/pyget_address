import json
import requests
from . modules import *

# 载入全局参数
conf = Config('D:\\workdata\\pyget_address\\config.json')

def getCarPath():
    '''根据提供的信息获取驾车路线规划'''

    http = conf.