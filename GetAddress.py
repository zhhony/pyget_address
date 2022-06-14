import json
import requests
from config import Config


# 载入全局参数
conf = Config('D:\\workdata\\pyget_address\\config.json')


def GetAddrSug(query: str, region: str = '北京市') -> list:
    """根据提供的地区关键字，以及地区权重，获取推荐的地区名称清单"""

    http = conf.getSuggestion
    output = conf.getOutput
    ak = conf.getAK
    https = http + 'query=' + query + '&region=' + \
        region + '&output=' + output+'&ak='+ak

    s = requests.session()
    re = s.post(https)
    reJson = re.text.encode('utf8')
    reJsonDict = json.loads(reJson)
    reJsinDictAdr = []
    for i in reJsonDict['result']:
        reJsinDictAdr.append(i['name'])
    return reJsinDictAdr


def GetLatitude(address: str,  region: str = '北京市'):
    """根据提供的地址返回对应的经纬度"""

    http = conf.getGeocode
    output = conf.getOutput
    ak = conf.getAK
    https = http + 'address=' + address + '&output=' + output + '&ak=' + ak

    s = requests.session()
    re = s.get(https)
    reJson = re.text.encode('utf8')
    reJsonDict = json.loads(reJson)
    results = reJsonDict['result']['location']
    results['precise'] = reJsonDict['result']['precise']
    results['confidence'] = reJsonDict['result']['confidence']
    results['comprehension'] = reJsonDict['result']['comprehension']
    results['level'] = reJsonDict['result']['level']
    return results


def GetAddress(query: str, tag: str, region: str = '北京市') -> any:
    """query:搜索关键字，如天安门
    tag:分类偏好，如美食
    regin:行政区域划分，如北京市
    """

    http = conf.getsearch
    output = conf.getOutput
    scope = conf.getScope
    pageSize = conf.getPageSize
    photoShow = conf.getPhotoShow
    ak = conf.getAK
    https = http + 'query=' + query + '&tag=' + tag + '&region=' + region + '&output=' + output + \
        '&scope=' + scope + '&page_size=' + pageSize + \
        '&photo_show=' + photoShow + '&ak=' + ak

    s = requests.Session()
    re = s.get(https)
    reJson = re.text.encode('utf-8')
    reJsoexinDict = json.loads(reJson)
    if reJsoexinDict['status'] == 0 and reJsoexinDict['total'] > 0:
        return reJsoexinDict['results']
    else:
        return '无法查询到详细信息'


def GetGeocode(location_lat: float, location_lng: float) -> str:

    http = conf.getReverseGeocode
    output = conf.getOutput
    extensionsTown = conf.getExtensionsTown
    ak = conf.getAK
    https = http + 'ak=' + ak + '&output=' + output + \
        '&extensions_town=' + extensionsTown + '&location=' + \
        str(location_lat) + ',' + str(location_lng)

    s = requests.session()
    re = s.get(https)
    reJson = re.text.encode('utf-8')
    reJsoexinDict = json.loads(reJson)
    if reJsoexinDict['status'] != 0:
        return '未查询到有效信息'
    else:
        return reJsoexinDict['result']['addressComponent']['town']
