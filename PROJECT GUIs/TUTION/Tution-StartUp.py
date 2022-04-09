import os
from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser


class Startup:
    '''This script is to execute Tution.exe on startup. Tution.exe is made
    when Tution.exe is compiled to exe using Pyinstaller or other similar
    script. This script is also to be compiled to exe'''

    def __init__(self):
        self.configFile = os.path.join(os.environ['USERPROFILE'], r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Tution\settings.ini')

    def AlterConfig(self):
        '''Edit config file with respective values'''

        dirpath = os.path.dirname(self.configFile)

        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        config = ConfigParser()
        config.read(self.configFile)

        if 'PATH' in config:
            status = True
            self.main_executable = config['PATH']['exe path']

        else:
            status = False

        config['STATUS'] = {'Startup': True}

        with open(self.configFile, 'w') as file:
            config.write(file)

        return status

    def main(self):
        '''Entry point of this script'''

        if self.AlterConfig():
            os.startfile(self.main_executable)

        else:  # When the config file is corrupt or does not exist
            root = Tk()
            root.withdraw()

            if messagebox.showinfo('TUTION', 'settings.ini is corrupted. Could\'t not execute Tution.exe.\n\nRun Tution.exe manually.') == 'ok':
                root.quit()
                root.destroy()

            root.mainloop()


if __name__ == '__main__':
    st = Startup()
    st.main()
