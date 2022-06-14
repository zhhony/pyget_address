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
        self.__log = CONFIG['log']

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
    def getExtensionsTown(self) -> str:
        return self.__extensions_town

    @property
    def getAK(self) -> str:
        return self.__ak

    @property
    def getLog(self) -> str:
        return self.__log