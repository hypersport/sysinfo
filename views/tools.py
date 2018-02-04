import socket
import psutil
from flask import Response, jsonify


def socket_prefix(prefix):
    return dict((getattr(socket, attr), attr) for attr in dir(socket) if attr.startswith(prefix))


socket_families = socket_prefix('AF_')
socket_types = socket_prefix('SOCK_')


def get_rlimits(process):
    return {
        'RLIMIT_AS': process.rlimit(psutil.RLIMIT_AS),
        'RLIMIT_CORE': process.rlimit(psutil.RLIMIT_CORE),
        'RLIMIT_CPU': process.rlimit(psutil.RLIMIT_CPU),
        'RLIMIT_DATA': process.rlimit(psutil.RLIMIT_DATA),
        'RLIMIT_FSIZE': process.rlimit(psutil.RLIMIT_FSIZE),
        'RLIMIT_LOCKS': process.rlimit(psutil.RLIMIT_LOCKS),
        'RLIMIT_MEMLOCK': process.rlimit(psutil.RLIMIT_MEMLOCK),
        'RLIMIT_MSGQUEUE': process.rlimit(psutil.RLIMIT_MSGQUEUE),
        'RLIMIT_NICE': process.rlimit(psutil.RLIMIT_NICE),
        'RLIMIT_NOFILE': process.rlimit(psutil.RLIMIT_NOFILE),
        'RLIMIT_NPROC': process.rlimit(psutil.RLIMIT_NPROC),
        'RLIMIT_RSS': process.rlimit(psutil.RLIMIT_RSS),
        'RLIMIT_RTPRIO': process.rlimit(psutil.RLIMIT_RTPRIO),
        'RLIMIT_RTTIME': process.rlimit(psutil.RLIMIT_RTTIME),
        'RLIMIT_SIGPENDING': process.rlimit(psutil.RLIMIT_SIGPENDING),
        'RLIMIT_STACK': process.rlimit(psutil.RLIMIT_STACK)
    }


# B to M
def b_to_m(value):
    return round(value / 1048576.0, 2)


class CustomResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)
