import os
import time
import shutil


class CLEAN_DESKTOP:
    '''Cleaning up the desktop by moving directories and files to directory named "CLEAN DESKTOP"'''

    def __init__(self):
        self.desktop_location = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        self.cleanup_location = os.path.join(self.desktop_location, 'CLEAN DESKTOP', time.strftime('%a %b %d %Y'))

    def get_file_number(self, basename, lists, is_file=False):
        ''' Suppose cleanup location have test.txt. And there is another test.txt in desktop.
            While moving the test.txt from the desktop ovewrites the test.txt of cleanup
            location. So inorder to fix this overwriting problem we need to rename the
            test.txt from desktop with some number adding to it eg: test(1).txt

            To fix this problem we need to:
                S1. First we need to get the numbering of the file.
                    Eg: test(4589).txt   ---->  4859

                S2. Add 1 to obtained next number
                    -----> 4859 + 1
                    -----> 4860

                S3. What if there is only test.txt in cleanup file. We need to declare 1
                    to the numbering variable '''

        if is_file:
            file_name = lists[-1].split('.')[0]

        else:
            file_name = lists[-1]

        file_number = file_name.strip(basename)[1:-1]  # S1

        if file_number:  # S2
            file_number = int(file_number) + 1

        else:  # S3
            file_number = 1

        return file_number

    def numbering_duplicate_files(self):
        '''If a file having same name exists both in desktop and self.cleaup_location then
           renaming it by adding certain number so that the same name conflicts disappears'''

        try:
            # Getting all files from desktop and cleanup_folder
            desktop_files = [f for f in os.listdir(self.desktop_location) if self.is_valid_file(f)]
            cleanup_files = os.listdir(self.cleanup_location)

            # Getting common files of desktop and cleanup folder
            common_files = [os.path.join(self.desktop_location, file) for file in desktop_files if file in cleanup_files]

            while common_files:
                file = common_files[0]
                basename = os.path.basename(file)

                if os.path.isdir(file):
                    # Geting all directories starting from basename of cleanup_files
                    dirs_starting_with_same_name = [f for f in cleanup_files if f.startswith(basename) and os.path.isdir(os.path.join(self.cleanup_location, f))]
                    dirs_starting_with_same_name.sort(key=len)

                    numbering = self.get_file_number(basename, dirs_starting_with_same_name)
                    new_name = f'{basename}({numbering})'

                else:
                    name, extension = tuple(basename.split('.'))

                    # Getting all files starting from name of cleanup_files
                    files_starting_with_same_name = [f for f in cleanup_files if f.startswith(name) and os.path.isfile(os.path.join(self.cleanup_location, f))]
                    files_starting_with_same_name.sort(key=len)

                    numbering = self.get_file_number(name, files_starting_with_same_name, True)
                    new_name = f'{name}({numbering}).{extension}'

                new_path = os.path.join(self.desktop_location, new_name)
                os.rename(file, new_path)

                del common_files[0]

        except FileNotFoundError:
            pass

    def check_folder(self):
        '''Checking if required folder exists. If not then creating it on the desktop'''

        if not os.path.exists(self.cleanup_location):
            os.makedirs(self.cleanup_location)

    def is_valid_file(self, file):
        '''Checks if the file type is not within the exclude_extensions list'''

        exclude_extensions = ['exe', 'ini', 'lnk']

        if file == 'CLEAN DESKTOP':   # Not including the cleanup folder itself
            return False

        for extension in exclude_extensions:
            if file.endswith(extension):
                return False

        return True

    def get_files(self):
        '''Getting file from the given location which is to be moved'''

        files = []

        for file in os.listdir(self.desktop_location):
            if self.is_valid_file(file):
                path = os.path.join(self.desktop_location, file)
                files.append(path)

        return files

    def main(self):
        '''Cleaning desktop'''

        self.numbering_duplicate_files()
        files = self.get_files()

        if files:
            self.check_folder()

            for moved_from in files:
                basename = os.path.basename(moved_from)
                moved_to = os.path.join(self.cleanup_location, basename)

                shutil.move(moved_from, moved_to)

            os.startfile(self.cleanup_location)


if __name__ == '__main__':
    cleanup = CLEAN_DESKTOP()
    cleanup.main()
