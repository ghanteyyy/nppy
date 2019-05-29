import os
import platform


def os_details():
    '''Returns some information regrading your Operating System (OS)'''

    print('''
    COMPUTER NAME           : {}
    USERNAME                : {}
    NUMBER OF PROCESSORS    : {}
    PROCESSOR IDENTIFIER    : {}
    OS                      : {}
    HOME DRIVE              : {}
    PROCESSOR LEVEL         : {}
    SYSTEMDRIVE             : {}
    SYSTEMROOT              : {}
    PROCESSOR ARCHITECTURE  : {}
    SYSTEM TYPE             : {}
    WINDOWS EDITION         : {}
        '''.format(os.environ['COMPUTERNAME'], os.environ['USERNAME'], os.environ['NUMBER_OF_PROCESSORS'],
                   os.environ['PROCESSOR_IDENTIFIER'], os.environ['OS'], os.environ['HOMEDRIVE'],
                   os.environ['PROCESSOR_LEVEL'], os.environ['SYSTEMDRIVE'], os.environ['SYSTEMROOT'],
                   os.environ['PROCESSOR_ARCHITECTURE'], platform.architecture()[0], platform.win32_ver()[0]))


if __name__ == '__main__':
    os_details()
