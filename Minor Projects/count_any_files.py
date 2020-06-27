import os


class Count_Files:
    '''Count number of files of given extension in a given path'''

    def __init__(self, path, extension):
        self.count = 0
        self.path = path
        self.extension = extension
        self.exclude = ['$RECYCLE.BIN', '$Recycle.Bin', '$SysReset', 'Config.Msi', 'Documents and Settings', 'ESD', 'hiberfil.sys', 'Intel', 'MSOCache',
                        'OneDriveTemp', 'pagefile.sys', 'PerfLogs', 'Program Files', 'Program Files (x86)', 'ProgramData', 'Python27', 'Recovery',
                        'swapfile.sys', 'System Volume Information', 'Windows', 'Public', '.idlerc', 'AppData', 'MicrosoftEdgeBackups', 'All Users']  # These directories is to be excluded.

    def is_path_valid(self):
        '''Check if the path given by the user is valid'''

        if not os.path.exists(self.path):
            raise FileNotFoundError(f'{self.path} does not exists')

        return True

    def main(self):
        '''Count files'''

        if self.is_path_valid():
            for dirs, dirn, files in os.walk(self.path):  # Going through all directories and files of the path
                for di in dirn:
                    if di in self.exclude:
                        dirn.remove(di)  # Removing directories if they are in self.exclude

                for f in files:
                    if f.endswith(self.extension):  # Checking if the obtained file has given extension
                        self.count += 1

            return f'\nPath: {self.path}\nNumber of .{self.extension} files: {self.count}'


if __name__ == '__main__':
    count = Count_Files(r'D:\My Project', 'jpg')
    print(count.main())
