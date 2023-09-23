import os
import sys
import winreg
from config import Config


class Startup:
    '''
    This class provides functionality to add an executable to the Windows startup
    programs. It is specifically designed to execute 'Tuition.exe' on startup,
    which is created by compiling 'Tuition.py' to an executable using tools like
    PyInstaller.
    '''

    def __init__(self):
        self.CONFIG = Config()
        self.MainExecutablePath = os.path.join(os.path.dirname(sys.executable), 'Tuition.exe')

    def AddToStartup(self):
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

        try:
            key = winreg.OpenKey(reg, f'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\Tuition', 0, winreg.KEY_WRITE)

        except WindowsError:
            key = winreg.OpenKey(reg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'Tuition', 0, winreg.REG_SZ, sys.executable)

        reg.Close()
        key.Close()

    def main(self):
        '''
        Entry point of this script
        '''

        if self.CONFIG.contents.get('Is-Added-To-Startup', False) is False:
            self.CONFIG.ToggleValues('Is-Added-To-Startup', True)

            self.AddToStartup()

        self.CONFIG.ToggleValues('From-StartUp', True)
        os.startfile(self.MainExecutablePath)


if __name__ == '__main__':
    st = Startup()
    st.main()
