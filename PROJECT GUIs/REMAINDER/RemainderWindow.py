import os
import sys
import time
import winreg

from tkinter import *
import pygame


class RemainderWindow:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.resource_path('tone.wav'))
        self.file_name = 'Remainder.txt'

    def window(self, text):
        '''
        GUI window
        '''

        self.root = Tk()
        self.root.withdraw()
        self.root.after(0, self.root.deiconify)
        self.root.resizable(0, 0)
        self.root.config(bg='red')
        self.root.overrideredirect(True)
        self.root.title('BIRTHDAY REMAINDER')
        self.root.wm_attributes('-topmost', 1)
        self.root.geometry(f'405x160+{self.root.winfo_screenwidth() - 406}+0')

        self.title = Label(self.root, text='REMAINDER', font=("Courier", 30), bg='red', fg='White')
        self.wishes = Label(self.root, text=text, font=("Courier", 15), bg='red', fg='White')
        self.close_button = Button(self.root, text='CLOSE', font=("Courier", 12), bg='red', activeforeground='white', activebackground='red', fg='White', width=10, relief='ridge', command=self.root.destroy)

        self.title.pack()
        self.wishes.pack()
        self.close_button.pack(side='bottom', pady=5)

        self.root.mainloop()

    def read_file(self):
        '''
        Getting contents of "Remainder.txt"
        '''

        with open(self.file_name, 'r') as f:
            return [line.strip('\n') for line in f.readlines()]

    def get_remainder(self):
        '''
        Getting remainders for today
        '''

        remainders = []
        remainder_time = time.strftime('%b %d')

        lines = self.read_file()

        for line in lines:
            if remainder_time in line:
                split = line.strip().split('|')
                remainder, rem_time = split[0].strip(), split[1].strip()

                remainders.append((remainder, rem_time))

        remainders.sort()
        return remainders

    def remove_remainder(self, remainder):
        '''
        Removing displayed remainders from files
        '''

        lines = self.read_file()
        check = ' | '.join(remainder)

        with open(self.file_name, 'w') as f:
            for line in lines:
                if check != line:
                    f.write(f'{line}\n')

    def main(self):
        '''
        Getting, showing and removing remainders
        '''

        try:
            while True:
                today_remainders = self.get_remainder()
                curr_time = time.strftime('%b %d %I %M %p')

                for remainder in today_remainders:
                    rem, rem_time = remainder[0], remainder[1]
                    split_rem_time = rem_time.split()

                    if curr_time == rem_time or (split_rem_time[2] == time.strftime('%I') and split_rem_time[3] < time.strftime('%M')) or (split_rem_time[2] < time.strftime('%I')):
                        pygame.mixer.music.play(-1)  # Playing Sound before showing remainder window and till user clicks close button.
                        self.window(rem)
                        pygame.mixer.music.stop()  # Stopping sound when user clicks close button.

                        self.remove_remainder(remainder)

                        today_remainders.remove(remainder)

        except FileNotFoundError:
            return

    def resource_path(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or
            file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or
            file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


class is_at_startup:
    '''
    Add the program path to startup
    '''

    def __init__(self, program_path):
        self.program_path = program_path
        self.program_basename = os.path.basename(self.program_path)

    def is_path_valid(self):
        '''
        Check if the given program path actually exists
        '''

        if os.path.exists(self.program_path):
            return True

        return False

    def main(self):
        '''
        Adding to startup
        '''

        if self.is_path_valid():
            areg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

            try:
                akey = winreg.OpenKey(areg, f'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\{self.program_basename}', 0, winreg.KEY_WRITE)
                areg.Close()
                akey.Close()

            except WindowsError:
                key = winreg.OpenKey(areg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, f'{self.program_basename}', 0, winreg.REG_SZ, f'{self.program_basename}')

                areg.Close()
                key.Close()


if __name__ == '__main__':
    path = os.path.realpath(__file__)
    startup = is_at_startup(path)
    startup.main()

    remind = RemainderWindow()
    remind.main()
