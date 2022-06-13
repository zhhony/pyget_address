def GetAddrSug(query: str, ak: str, region: str = '北京市') -> list:
    """根据提供的地区关键字，以及地区权重，获取推荐的地区名称清单"""
    import json
    import requests

    http = 'https://api.map.baidu.com/place/v2/suggestion?'
    output = 'json'
    https = http + 'query=' + query + '&region=' + \
        region + '&output=' + output+'&ak='+ak

    s = requests.session()
    re = s.post(https)
    reJson = re.text.encode('utf8')
    reJsonDict = json.load(reJson)
    reJsinDictAdr = []
    for i in reJsonDict['result']:
        reJsinDictAdr.append(i['name'])
    return reJsinDictAdr


def GetLatitude(address: str, ak: str, region: str = '北京市'):
    '''根据提供的地址返回对应的经纬度'''
    import json
    import requests

    http = 'https://api.map.baidu.com/geocoding/v3/?'
    output = 'json'
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


def GetAddress(query: str, tag: str, ak: str, region: str = '北京市', type='address'):
    '''type:address详细地区、province省、city市、area区、location经纬度、all全部信息'''
    import json
    import requests

    http = 'https://api.map.baidu.com/place/v2/search?'
    output = 'json'
    scope = '2'
    page_size = '20'
    photo_show = 'false'
    https = http + 'query=' + query + '&tag=' + tag + '&region=' + region + '&output=' + output + \
        '&scope=' + scope + '&page_size=' + page_size + \
        '&photo_show=' + photo_show + '&ak=' + ak

    s = requests.Session()
    re = s.get(https)
    reJson = re.text.encode('utf-8')
    reJsoexinDict = json.loads(reJson)
    if reJsoexinDict['status'] == 0 and reJsoexinDict['total'] > 0:
        if type == 'all':
            return reJsoexinDict
        else:
            return reJsoexinDict['results'][0][type]
    else:
        return '无法查询到详细信息'


def GetGeocode(location_lat, location_lng, ak):
    import json
    import requests

    http = 'https://api.map.baidu.com/reverse_geocoding/v3/?'
    output = 'json'
    extensions_town = 'true'

    https = http + 'ak=' + ak + '&output=' + output + \
        '&extensions_town=' + extensions_town + '&location=' + \
        str(location_lat) + ',' + str(location_lng)

    s = requests.session()
    re = s.get(https)
    reJson = re.text.encode('utf-8')
    reJsoexinDict = json.loads(reJson)
    if reJsoexinDict['status'] != 0:
        return '未查询到有效信息'
    else:
        return reJsoexinDict['result']['addressComponent']['town']
