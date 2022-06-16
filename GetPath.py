import json
import traceback
import requests
from . modules import *
import sys

# 载入全局参数
conf = Config('D:\\workdata\\pyget_address\\config.json')

# 定义一个用于反馈API接口成功接入但是返回异常的错误类


class PostError(Exception):
    pass


def getCarPath(plate_number: str, tactics: int, origin: tuple, destination: tuple, *waypoints: list):
    '''根据提供的信息获取驾车路线规划,并将详细信息存入config文件所定位的log文件夹中\n
    plate_number：车牌号\n
    origin：起点经纬度\n
    destination：终点经纬度\n
    waypoints：途径点经纬度组，最多18个。\n
    tactics：\n
    0：默认
    2：距离最短
    3：不走高速
    4：高速优先
    5：躲避拥堵
    6：少收费
    7: 躲避拥堵 & 高速优先
    8: 躲避拥堵 & 不走高速
    9: 躲避拥堵 & 少收费
    10: 躲避拥堵 & 不走高速 & 少收费
    11: 不走高速 & 少收费
    12: 距离优先（考虑限行和路况，距离相对短且不一定稳定）
    '''

    http = conf.getDriving
    ak = conf.getAK
    cartype = conf.getCartype
    originStr = ','.join([str(i) for i in origin])
    destinationStr = ','.join([str(i) for i in destination])
    if waypoints != None:
        for index in range(len(waypoints)):
            waypoints[index] = ','.join([str(i) for i in waypoints[index]])
        waypointsStr = '|'.join(waypoints)
    else:
        waypointsStr = ''

    https = http + 'origin=' + originStr + '&destination=' + destinationStr + '&ak=' + ak + '&cartype=' + \
        str(cartype) + '&waypoints=' + waypointsStr + \
        '&plate_number=' + plate_number + '&tactics=' + str(tactics)
    try:
        s = requests.session()
        re = s.get(https)
        reJson = re.text.encode('utf8')
        reJsonDict = json.loads(reJson)
        if reJsonDict['status'] != 0:
            raise PostError
    except PostError:
        print('API返回了错误的信息\n错误码：%s\n错误信息：%s' %
              (reJsonDict['status'], reJsonDict['message']))
        return None
    except:
        print("GET阶段发生了未知的异常")
        a,b,c = sys.exc_info()
        print("异常类：%s"%a)
        print("异常信息：%s"%b)
        print("\n传播路径:")
        traceback.print_tb(c)
        return None
    else:
        with open(conf.getLog + 'getCarPath_' + TimeStamp() + '.json', 'w') as file:
            file.write(json.dumps(
                reJsonDict['result'], ensure_ascii=False, sort_keys=False, indent=True))
        return reJsonDict['result']
    finally:
        pass

# from pyget_address import *
# importlib.reload(pyget_address)
# pyget_address.getCarPath('苏B37F34',3,(40.01116,116.339303),(39.936404,116.452562))
