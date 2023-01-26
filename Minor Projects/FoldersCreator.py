import os
import string
import random


class FoldersCreator:
    '''
    Create n number of folders
    '''

    def __init__(self, path, number_of_folders=100, name_length=8):
        self.path = path
        self.name_length = name_length
        self.number_of_folders = number_of_folders

    def is_path_valid(self):
        '''
        Check if the path given by the user actually exists
        '''

        split_path = os.path.split(self.path)[0]

        if os.path.exists(split_path):
            if os.path.exists(self.path) is False:
                os.mkdir(self.path)

            return True

        else:
            raise FileNotFoundError(f'{self.path} does not exists')

    def random_name(self):
        '''
        Generating random name for each folder
        '''

        return ''.join([random.choice(string.printable[:62]) for _ in range(self.name_length)])

    def main(self):
        '''
        Creating folders as per the number_of_folders provided by the user
        '''

        if self.is_path_valid():
            for _ in range(self.number_of_folders):
                random_name = self.random_name()

                path = os.path.join(self.path, random_name)
                os.mkdir(path)

            os.startfile(self.path)


if __name__ == '__main__':
    path = os.path.join(os.path.realpath('.'), '100folders')

    folders = FoldersCreator(path)
    folders.main()
