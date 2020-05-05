from datetime import datetime
from .tools import socket_families, socket_types

B_TO_G = 1073741824.0
B_TO_M = 1048576.0
B_TO_K = 1024.0


def format_time(value, date_format='%Y-%m-%d %H:%M:%S'):
    dt = datetime.fromtimestamp(int(value))
    return dt.strftime(date_format)


def format_size(value):
    tmp = value / B_TO_G
    if tmp < 1.0:
        tmp = value / B_TO_M
        if tmp < 1.0:
            tmp = value / B_TO_K
            return "%s K" % round(tmp, 2)
        return "%s M" % round(tmp, 2)
    return "%s G" % round(tmp, 2)


def socket_family(value):
    return socket_families[value]


def socket_type(value):
    return socket_types[value]


def format_addr_port(value):
    if value:
        result = value[0] + ':' + str(value[1])
    else:
        result = ''

    return result
