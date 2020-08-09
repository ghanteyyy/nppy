import os

try:   # Python 3
    import winreg

except ModuleNotFoundError:   # Python 2
    import _winreg as winreg


class is_at_startup:
    '''Adding the given program path to startup'''

    def __init__(self, program_path):
        self.program_path = program_path
        self.program_basename = os.path.basename(self.program_path)

    def main(self):
        '''Adding to startup'''

        if os.path.exists(self.program_path):
            areg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

            try:
                akey = winreg.OpenKey(areg, f'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\{self.program_basename}', 0, winreg.KEY_WRITE)
                areg.Close()
                akey.Close()

                print(f'{self.program_path} already at startup')

            except WindowsError:
                key = winreg.OpenKey(areg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, f'{self.program_basename}', 0, winreg.REG_SZ, f'{self.program_basename}')

                areg.Close()
                key.Close()

                print(f'{self.program_path} added to startup')


if __name__ == '__main__':
    startup = is_at_startup('your program path')
    startup.main()
