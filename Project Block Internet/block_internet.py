import sys
import ctypes
from datetime import datetime as dt


class Block_Internet:
    '''Blocks internet access to the provided sites '''

    def __init__(self, starting_time=10, ending_time=17):
        self.newline = False
        self.localhost = '127.0.0.1'
        self.site_file = 'sites.txt'
        self.ending_time = ending_time
        self.starting_time = starting_time
        self.host_file = r'C:\Windows\System32\drivers\etc\hosts'

    def is_admin(self):
        '''Check if your program has ran in administrative mode or not'''

        try:
            return ctypes.windll.shell32.IsUserAnAdmin()

        except:
            return False

    def is_working_hour(self):
        '''Checking if it is still working hour'''

        if dt(dt.now().year, dt.now().month, dt.now().day, self.starting_time) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, self.ending_time):
            return True

        return False

    def read_file(self, file):
        '''Reading hosts file'''

        with open(file, 'r') as f:
            lines = [file.strip('\n') for file in f.readlines()]

            return lines

    def remove_last_newlines(self):
        '''Removing all blank_lines from the files'''

        with open(self.host_file, 'r') as f:
            contents = f.read().strip('\n')

        with open(self.host_file, 'w') as f:
            f.write(contents)

    def main(self):
        '''Blocking internet'''

        lines = self.read_file(self.host_file)
        sites = self.read_file(self.site_file)

        if self.is_working_hour():
            with open(self.host_file, 'a') as f:
                if not self.newline:
                    f.write('\n')
                    self.newline = True

                for site in sites:
                    exclude = f'{self.localhost} \t{site}'

                    if exclude not in lines:    # writing 127.0.0.1 "site name" to the file if there is not which means no access to that site
                        f.write(f'{exclude}\n')

        else:
            with open(self.host_file, 'w') as f:
                for line in lines:
                    if not line.startswith(self.localhost):   # Removing all added sites
                        f.write(f'{line}\n')

            self.newline = False
            self.remove_last_newlines()


if __name__ == '__main__':
    run = True
    block_internet = Block_Internet()

    if block_internet.is_admin():
        while run:
            block_internet.main()

    else:
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, __file__, None, 1)
