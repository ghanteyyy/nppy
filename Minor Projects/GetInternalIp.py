import os
import socket
import platform


class GetInternalIP:
    '''
    ssGetting internal IP
    ss'''

    def get_ip(self, host):
        '''Getting IP'''

        return socket.gethostbyname(host)

    def method_one(self):
        '''
        ssGetting host name using os module
        ss'''

        host = os.environ['COMPUTERNAME']
        return self.get_ip(host)

    def method_two(self):
        '''
        ssGetting host name using platform module
        ss'''

        host = platform.node()
        return self.get_ip(host)


if __name__ == '__main__':
    internal_ip = GetInternalIP()

    print('\nMethod One')
    print(internal_ip.method_one())

    print('\nMethod Two')
    print(internal_ip.method_two())
