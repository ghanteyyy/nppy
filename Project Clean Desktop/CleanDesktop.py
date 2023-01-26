import os
import time
import shutil


class CleanDesktop:
    '''
    Cleaning up the desktop by moving directories and files to directory
    named "CLEAN DESKTOP"
    '''

    def __init__(self):
        self.exclude_extensions = ['ini', 'lnk']
        self.desktop_location = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        self.exclude_directories = ['CLEANUP DESKTOP', 'My Projects', 'Tor Browser']

    def create_today_directory(self):
        '''
        Create directory as per today's date inside "CLEAN DESKTOP" directory
        '''

        today_date = time.strftime('%a %b %m %Y')
        self.cleanup_location = os.path.join(self.desktop_location, 'CLEANUP DESKTOP', today_date)

        if not os.path.exists(self.cleanup_location):
            os.makedirs(self.cleanup_location)

    def is_valid_file(self, file):
        '''
        Checks if the file type is not within the exclude_extensions list
        '''

        file = os.path.basename(file)

        if file in self.exclude_directories:   # Not including the cleanup folder itself
            return False

        for extension in self.exclude_extensions:
            if file.endswith(extension):
                return False

        return True

    def get_common_files_or_directories(self):
        '''
        Get common files that are in desktop and the cleanup locations
        '''

        desktop_files = set(os.listdir(self.desktop_location))
        cleanup_files = set(os.listdir(self.cleanup_location))
        common_files = [os.path.join(self.desktop_location, f) for f in desktop_files.intersection(cleanup_files)]

        return [f for f in common_files if self.is_valid_file(f)]

    def rename_common_files(self):
        '''
        Rename files or directories if they exists in desktop and cleanup directories
        '''

        common_files = self.get_common_files_or_directories()

        for file in common_files:
            if self.is_valid_file(file):
                new_name = self.extract_file_number(file)
                os.rename(file, new_name)

    def extract_file_number(self, file):
        '''
        Extract file_number having same name of **file** parameter's basename
        and add 1 to it
        '''

        _dir, basename = os.path.split(file)
        file_name = basename.split('.')[0]

        if os.path.isfile(file):
            extension = '.' + basename.split('.')[0]
            file_with_same_names = [f for f in os.listdir(self.cleanup_location) if f.startswith(file_name) and os.path.isfile(os.path.join(self.cleanup_location, f))]

        else:
            extension = ''
            file_with_same_names = [f for f in os.listdir(self.cleanup_location) if f.startswith(basename) and os.path.isdir(os.path.join(self.cleanup_location, f))]

        file_with_same_names.sort(key=len)
        last_file_name = file_with_same_names[-1].split('.')[0]  # Removing file extension
        file_number = last_file_name.replace(file_name, '')[1:-1]

        if file_number.isdigit():
            file_number = str(int(file_number) + 1)

            split = last_file_name.split('(')
            split[-1] = file_number
            new_name = f'{"(".join(split)}){extension}'

        else:
            file_number = '1'
            new_name = f'{last_file_name}({file_number}){extension}'

        return os.path.join(_dir, new_name)

    def main(self):
        '''
        Cleaning desktop
        '''

        self.create_today_directory()
        self.rename_common_files()

        desktop_files = [os.path.join(self.desktop_location, f) for f in os.listdir(self.desktop_location)]

        for file in desktop_files:
            if self.is_valid_file(file):
                move_to = os.path.join(self.cleanup_location, os.path.basename(file))
                shutil.move(file, move_to)

        os.startfile(self.cleanup_location)


if __name__ == '__main__':
    cleanup = CleanDesktop()
    cleanup.main()
