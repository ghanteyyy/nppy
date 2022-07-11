import sys
import ctypes
from datetime import datetime as dt


class BlockInternet:
    '''Blocks INTERNET access to the provided sites '''

    def __init__(self, starting_time=10, ending_time=17):
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

        return dt(dt.now().year, dt.now().month, dt.now().day, self.starting_time) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, self.ending_time)

    def read_file(self, file):
        '''Reading hosts file'''

        with open(file, 'r') as f:
            return [line.strip('\n') for line in f.readlines() if line.strip('\n')]

    def write_file(self, contents):
        '''Writing site with localhost in the host-file'''

        is_newline = False

        with open(self.host_file, 'w') as f:
            for content in contents:
                if content.startswith(self.localhost) and not is_newline:  # Adding newline before adding any site in the host_file
                    f.write(f'\n{content}\n')
                    is_newline = True

                else:
                    f.write(f'{content}\n')

    def main(self):
        '''Blocking INTERNET'''

        lines = self.read_file(self.host_file)
        sites = self.read_file(self.site_file)

        if self.is_working_hour():
            for site in sites:
                exclude = f'{self.localhost} \t{site}'

                if exclude not in lines:
                    lines.append(exclude)

        else:
            lines = [line for line in lines if not line.startswith(self.localhost)]

        self.write_file(lines)


if __name__ == '__main__':
    block_internet = BlockInternet()

    if block_internet.is_admin():
        while True:
            block_internet.main()

    else:
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, __file__, None, 1)
