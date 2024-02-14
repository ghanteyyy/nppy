import os
import sys
import winreg
import psutil
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

    def AddToStartup(self):
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

        try:
            key = winreg.OpenKey(reg, f'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\Tuition', 0, winreg.KEY_WRITE)

        except WindowsError:
            key = winreg.OpenKey(reg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'Tuition', 0, winreg.REG_SZ, sys.executable)

        reg.Close()
        key.Close()

    def CheckIfMainExecutableIsRunning(self):
        '''
        Check if Tuition.exe is running
        '''

        return "Tuition.exe" in (p.name() for p in psutil.process_iter())

    def main(self):
        '''
        Entry point of this script
        '''

        if self.CONFIG.contents.get('Is-Added-To-Startup', False) is False:
            self.CONFIG.ToggleValues('Is-Added-To-Startup', True)

            self.AddToStartup()

        is_main_executable_running = self.CheckIfMainExecutableIsRunning()

        if is_main_executable_running is False:
            self.CONFIG.SetDefaultValues()
            self.CONFIG.ToggleValues('From-StartUp', True)
            self.CONFIG.ToggleValues('Is-Minimized', True)

            main_executable_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Tuition.exe')

            if os.path.exists(main_executable_path):
                os.startfile(main_executable_path)


if __name__ == '__main__':
    st = Startup()
    st.main()
