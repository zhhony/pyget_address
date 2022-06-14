import json
import requests
from .pytimestamp import TimeStamp
from .pyconfig import Config


# 载入全局参数
conf = Config('D:\\workdata\\pyget_address\\config.json')


def GetSuggest(query: str, region: str = '北京市') -> list:
    """根据提供的地区关键字，以及地区权重，检索某一行政区划内（目前最细到城市级别）的地点信息。\n
    query:检索关键字。行政区划区域检索不支持多关键字检索。
    region:检索行政区划区域,增加区域内数据召回权重。
    """

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


def GetLatitude(address: str,  city: str = '北京市') -> any:
    """根据提供的结构化地址数据（如：北京市海淀区上地十街十号）转换为对应坐标点（经纬度）。\n
    address:待解析的地址。最多支持84个字节。
    city:地址所在的城市名。用于指定上述地址所在的城市，当多个城市都有上述地址时，该参数起到过滤作用，但不限制坐标召回城市。
    """

    http = conf.getGeocode
    output = conf.getOutput
    ak = conf.getAK
    https = http + 'address=' + address + '&output=' + \
        output + '&ak=' + ak + '&city=' + city

    s = requests.session()
    re = s.get(https)
    reJson = re.text.encode('utf8')
    reJsonDict = json.loads(reJson)
    results = reJsonDict['result']['location']
    results['precise'] = reJsonDict['result']['precise']  # 1表示精确，0表示模糊
    results['confidence'] = reJsonDict['result']['confidence']  # 打点误差范围
    # 服务器对地址的理解程度0-100，100表示完全理解
    results['comprehension'] = reJsonDict['result']['comprehension']
    results['level'] = reJsonDict['result']['level']  # 理解出来的地址类型
    return results


def GetSearch(query: str, tag: str, region: str = '北京市') -> any:
    """本函数可通过接口获取地点（POI）基础或详细地理信息。函数返回查询到的条目数，并将详细结果保存到config文件所配置的log路径中。
    注意，虽然本函数最多能查询150条记录，但是受限于篇幅，将仅仅转存前20条记录。\n
    query:搜索关键字，如天安门
    tag:分类偏好，如美食
    regin:行政区域划分，如北京市
    """

    http = conf.getsearch
    output = conf.getOutput
    scope = conf.getScope
    pageSize = conf.getPageSize
    pageNum = conf.getPageNum
    photoShow = conf.getPhotoShow
    ak = conf.getAK
    https = http + 'query=' + query + '&tag=' + tag + '&region=' + region + '&output=' + output + \
        '&scope=' + scope + '&page_size=' + pageSize + '&page_num=' + pageNum +\
        '&photo_show=' + photoShow + '&ak=' + ak

    s = requests.Session()
    re = s.get(https)
    reJson = re.text.encode('utf-8')
    reJsoexinDict = json.loads(reJson)

    total = reJsoexinDict['total']  # 总记录数
    if reJsoexinDict['status'] == 0 and total > 0:
        with open(conf.getLog + 'GetSearch_' + TimeStamp() + '.json', 'w') as file:
            file.write(json.dumps(
                reJsoexinDict['results'], ensure_ascii=False, sort_keys=False, indent=True))
        return '共返回 %s 条记录' % total
    else:
        return '无法查询到详细信息'


def GetGeocode(location_lat: float, location_lng: float) -> str:
    """本函数用于利用提供的经纬度获取相应的地理信息并返回格式化地址信息（省、市、区&县、镇&路）。详细结果将保存在config文件所配置的log路径中。
    逆地理编码服务提供将坐标点（经纬度）转换为对应位置信息（如所在行政区划，周边地标点分布）功能。\n
    location_lat：地理经度，小数类型。
    location_lng：地理纬度，小数类型。
    """

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
        with open(conf.getLog + 'GetGeocode_' + TimeStamp() + '.json', 'w') as file:
            file.write(json.dumps(
                reJsoexinDict['result'], ensure_ascii=False, sort_keys=False, indent=True))
        return reJsoexinDict['result']['formatted_address']
