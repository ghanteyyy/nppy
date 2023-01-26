import os
import subprocess


class GetMACAddress:
    '''
    Getting all MAC address
    '''

    def __init__(self):
        self.command = 'getmac'

    def method_one(self):
        '''
        Using os module
        '''

        try:
            mac = os.system(self.command).read()
            print(mac)

        except AttributeError:
            pass

    def method_two(self):
        '''
        Using subprocess module
        '''

        mac = subprocess.check_output(self.command, encoding='utf-8', creationflags=0x08000000)
        print(mac)


mac = GetMACAddress()

print('\nMethod One')
mac.method_one()

print('\nMethod Two')
mac.method_two()
