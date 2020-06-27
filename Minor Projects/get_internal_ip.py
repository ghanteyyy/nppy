import os
import socket
import platform


class Internal_IP:
    '''Getting internal IP'''

    def get_ip(self, host):
        '''Getting IP'''

        return socket.gethostbyname(host)

    def method_one(self):
        '''Getting host name using os module.'''

        host = os.environ['COMPUTERNAME']
        return self.get_ip(host)

    def method_two(self):
        '''Getting host name using platform module.'''

        host = platform.node()
        return self.get_ip(host)


if __name__ == '__main__':
    internal_ip = Internal_IP()

    print('\nMethod One')
    print(internal_ip.method_one())

    print('\nMethod Two')
    print(internal_ip.method_two())
