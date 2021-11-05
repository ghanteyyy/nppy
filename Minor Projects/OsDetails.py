import os
import platform


def OSDetails():
    '''Returns some information regrading your Operating System (OS)'''

    print(f'''
    COMPUTER NAME                      : {os.environ['COMPUTERNAME']}
    USERNAME                           : {os.environ['USERNAME']}
    NUMBER OF PROCESSORS               : {os.environ['NUMBER_OF_PROCESSORS']}
    PROCESSOR IDENTIFIER               : {os.environ['PROCESSOR_IDENTIFIER']}
    OS                                 : {os.environ['OS']}
    HOME DRIVE/SYSTEMDRIVE             : {os.environ['HOMEDRIVE']}
    PROCESSOR LEVEL                    : {os.environ['PROCESSOR_LEVEL']}
    SYSTEMROOT                         : {os.environ['SYSTEMROOT']}
    PROCESSOR ARCHITECTURE             : {os.environ['PROCESSOR_ARCHITECTURE']}
    SYSTEM TYPE                        : {platform.architecture()[0]}
    WINDOWS EDITION                    : {platform.win32_ver()[0]}''')


if __name__ == '__main__':
    OSDetails()
