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
            While moving the test.txt from the desktop overwrites the test.txt of cleanup
            location. So in-order to fix this overwriting problem we need to rename the
            test.txt from desktop with some number adding to it eg: test(1).txt

            To fix this problem we need to:
                S1. First we need to get the numbering of the file.
                    Eg: test(4589).txt   ---->  4859

                S2. Add 1 to obtained next number
                    -----> 4859 + 1
                    -----> 4860

                S3. What if there is only test.txt in cleanup file. We need to declare 1
                    to the numbering variable

            In short: This function returns number if the same file / directory
                      already exists in the cleanup directory to avoid overwrite
                      those files / directories.'''

        file_number = False
        lists.sort(key=len)

        while not file_number:
            try:
                if is_file:
                    file_name = lists[-1].split('.')[0]

                else:
                    file_name = lists

                file_number = file_name.replace(basename, '')[1:-1].strip()  # S1

                if file_number:  # S2
                    file_number = int(file_number) + 1

                else:  # S3
                    file_number = 1

            except ValueError:
                ''' Suppose we have a file having named "test(1)(1).txt" then when extracting
                    file_number we get 1)(1) which is not a number obviously so, ValueError
                    kicks in. Inorder to fix this problem we need to check each value
                    from the **lists** parameter removing the last value from ii until
                    we get the valid file_number.'''

                lists = lists[:-1]
                file_number = False

        return file_number

    def rename_path(self, file, lists):
        '''Renames old_path with new path after adding number to the duplicate
           files or directories before cleaning up the desktop'''

        basename = os.path.basename(file)

        if os.path.isfile(file):
            name, extension = tuple(basename.split('.'))

            lists = [f for f in lists if name in f]

            numbering = self.get_file_number(name, lists, True)
            new_name = f'{name}({numbering}).{extension}'

        else:
            lists = [f for f in lists if basename in f]

            numbering = self.get_file_number(basename, lists, False)
            new_name = f'{basename}({numbering})'

        new_path = os.path.join(self.desktop_location, new_name)
        os.rename(file, new_path)

    def numbering_duplicate_files(self):
        ''' If a file having same name exists both in desktop and self.cleaup_location then
            renaming it by adding certain number so that the same name conflicts disappears'''

        try:
            desktop_files = [f for f in os.listdir(self.desktop_location) if self.is_valid_file(f)]
            cleanup_files = os.listdir(self.cleanup_location)

            common_files = [os.path.join(self.desktop_location, file) for file in desktop_files if file in cleanup_files]

            for file in common_files:
                try:
                    self.rename_path(file, cleanup_files)

                except FileExistsError:
                    ''' Suppose you have "test" directory in cleanup directory and again you ended
                        up having "test" directory as well as "test(1)" directory in the desktop
                        and when renaming the "test" directory in desktop FileExistsError gets
                        triggered because "test" directory tends to rename to "test(1)" but
                        we already have the same name in desktop. So, to fix this problem
                        we need to extract the numbers from test(1) and add 1 to it and
                        then rename 'test' directory with the obtained number.

                        Same logics is applied when we don't encounter FileExistsError.
                        So, when we don't get FileExistsError we check duplicates
                        in cleanup_file but when we do encounter then we check
                        in desktop_files.

                        Thus, we pass cleanup_files as lists parameter in rename_path
                        function when we don't encounter FileExistsError and
                        desktop_files as lists parameter when we get
                        encounter.'''

                    self.rename_path(file, desktop_files)

        except FileNotFoundError:
            ''' When the script runs for the first time in a day, the cleanup
                directory does not exists yet so FileNotFoundError triggers.
                So we just skp it with a pass.'''

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

    def main(self):
        '''Cleaning desktop'''

        self.numbering_duplicate_files()
        files = [os.path.join(self.desktop_location, f) for f in os.listdir(self.desktop_location) if self.is_valid_file(f)]

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
