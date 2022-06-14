from datetime import datetime
"""用于产生一组13位的时间戳"""


def TimeStamp() -> str:
    __timestamp = str(datetime.timestamp(
        datetime.now()))  # 取本地时间并转化 float->str
    __timestamp = __timestamp.replace(
        '.', '') + '000000'  # 将 . 去掉，并用0补位,防止出现没有小数点的情况
    __timestamp = __timestamp[:13]  # 从左边开始取13位作为最终的时间戳
    return __timestamp
