import os

try:   # Python 2
    from _winreg import ConnectRegistry, HKEY_CURRENT_USER, OpenKey, KEY_WRITE, SetValueEx, REG_SZ, KEY_SET_VALUE

except (ImportError, ModuleNotFoundError):   # Python 3
    from winreg import ConnectRegistry, HKEY_CURRENT_USER, OpenKey, KEY_WRITE, SetValueEx, REG_SZ, KEY_SET_VALUE


def is_at_startup(program_path):
    '''Add any program to your startup list'''

    areg = ConnectRegistry(None, HKEY_CURRENT_USER)

    try:
        akey = OpenKey(areg, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\{}'.format(os.path.basename(program_path)), 0, KEY_WRITE)
        areg.Close()
        akey.Close()

    except WindowsError:
        key = OpenKey(areg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, KEY_SET_VALUE)
        SetValueEx(key, '{}'.format(os.path.basename(program_path)), 0, REG_SZ, '{}'.format(program_path))

        areg.Close()
        key.Close()

        print('{} added to startup'.format(os.path.basename(program_path)))


if __name__ == '__main__':
    is_at_startup('your program path')
