import json
import requests
from . modules import *

# 载入全局参数
conf = Config('D:\\workdata\\pyget_address\\config.json')


def getCarPath(plate_number: str, tactics: int, origin: tuple, destination: tuple, *waypoints: list):
    '''根据提供的信息获取驾车路线规划\n
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

    https = http + 'origin=' + originStr + '&destination=' + destinationStr + '&ak=' + ak + '&cartype=' + \
        cartype + '&waypoints=' + waypointsStr + \
        '&plate_number=' + plate_number + '&tactics=' + str(tactics)

    s = requests.session()
    re = s.get(https)
    reJson = re.text.encode('utf8')
    reJsonDict = json.loads(reJson)
    return reJsonDict


# getCarPath('苏B37F34',3,(40.01116,116.339303),(39.936404,116.452562))
