import socket


def socket_prefix(prefix):
    return dict((getattr(socket, attr), attr) for attr in dir(socket) if attr.startswith(prefix))


socket_families = socket_prefix('AF_')
socket_types = socket_prefix('SOCK_')
