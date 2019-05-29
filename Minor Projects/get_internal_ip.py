# import os
# import platform
import socket


def get_internal_ip():
    host_name = socket.gethostname()

    '''You can get host_name is next three ways:
            host_name = os.environ['COMPUTERNAME']
            host_name = os.environ['DOMAINNAME']
            host_name = platform.node() '''

    get_ip = socket.gethostbyname(host_name)
    print(get_ip)


if __name__ == '__main__':
    get_internal_ip()
