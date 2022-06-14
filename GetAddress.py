import json
import requests
import pyjson_withcommit


# 新增参数类，读取本地全局参数
class Config:
    def __init__(self, configPath: str) -> None:
        CONFIG = pyjson_withcommit.LoadJson(configPath)
        self.__geocode = CONFIG['http']['geocode']
        self.__suggestion = CONFIG['http']['suggestion']
        self.__search = CONFIG['http']['search']
        self.__reverse_geocode = CONFIG['http']['reverse_geocode']
        self.__output = CONFIG['output']
        self.__scope = CONFIG['scope']
        self.__page_size = CONFIG['page_size']
        self.__photo_show = CONFIG['photo_show']
        self.__extensions_town = CONFIG['extensions_town']
        self.__ak = CONFIG['ak']

    @property
    def getGeocode(self) -> str:
        return self.__geocode

    @property
    def getSuggestion(self) -> str:
        return self.__suggestion

    @property
    def getsearch(self) -> str:
        return self.__search

    @property
    def getReverseGeocode(self) -> str:
        return self.__reverse_geocode

    @property
    def getOutput(self) -> str:
        return self.__output

    @property
    def getScope(self) -> str:
        return self.__scope

    @property
    def getPageSize(self) -> str:
        return self.__page_size

    @property
    def getPhotoShow(self) -> str:
        return self.__photo_show

    @property
    def getExtensions_Town(self) -> str:
        return self.__extensions_town

    @property
    def getAK(self) -> str:
        return self.__ak


# 载入全局参数
conf = Config('D:\\workdata\\pyget_address\\config\config.json')


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
    reJsonDict = json.load(reJson)
    reJsinDictAdr = []
    for i in reJsonDict['result']:
        reJsinDictAdr.append(i['name'])
    return reJsinDictAdr


def GetLatitude(address: str,  region: str = '北京市'):
    '''根据提供的地址返回对应的经纬度'''

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


def GetAddress(query: str, tag: str, ak: str, region: str = '北京市', type='address'):
    '''type:address详细地区、province省、city市、area区、location经纬度、all全部信息'''

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
