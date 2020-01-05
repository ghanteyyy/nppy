'''Blocks access to the provided sites '''


import sys
import ctypes
from datetime import datetime as dt


def is_admin():
    '''Execute your program with administrator privilege'''

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()

    except:
        return False


if is_admin():
    hosts = r'C:\Windows\System32\drivers\etc\hosts'
    sites = ['www.facebook.com', 'facebook.com', 'fb.com', 'www.fb.com', 'www.google.com']

    while True:
        if dt(dt.now().year, dt.now().month, dt.now().day, 10) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, 21):
            with open(hosts, 'r+') as host:
                lines = host.read()
                host.write('\n')

                for site in sites:
                    if site not in lines:
                        host.write('127.0.0.1 \t{}\n'.format(site))

        else:
            with open(hosts, 'r+') as host:
                lines = host.readlines()
                host.seek(0)

                for line in lines:
                    if not line.startswith('127.0.0.1') and len(line.strip('\n')) != 0:
                        host.write(line)

                    ''' You can also use following for line 39:
                            if not any(site in line for site in sites) '''

                host.truncate()

else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, __file__, None, 1)
