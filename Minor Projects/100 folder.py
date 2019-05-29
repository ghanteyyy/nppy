import os
import string
import random
import getpass


def hunderd_folders(number_of_folders, length_of_folder_name):
    '''Create 'n' number of folders inside python_FOLDER in your desktop'''

    try:
        path = 'C:\\Users\\{}\\Desktop\\python_Folder'.format(getpass.getuser())

        if not os.path.exists(path):   # Checking if path exists
            os.mkdir(os.path.join(path))    # If path does not exist then creates it

        folder_name = ''     # No name yet.

        for _ in range(number_of_folders):     # Loop for creating folders
            for _ in range(length_of_folder_name):    # Loop to generate random folder name
                x = random.randint(0, 61)   # Generate random number between 0 to 61
                folder_name += string.printable[x]   # Slicing a character from string.printable with value 'x'

            os.mkdir(os.path.join(path, folder_name))    # Joining path and random generated name and creating folder.
            folder_name = ''   # Emptying folder_name for another new name

        os.startfile(path)

    except (ValueError, NameError):
        print('Number of folders and length of folder name is expected in integer')

    except KeyboardInterrupt:
        pass

    '''PYTHONIC way:

            [CODE]
                path = 'C:\\Users\\{}\\Desktop\\Python Generated Folder'.format(getpass.getuser())

                if not os.path.exists(path):
                    os.mkdir(os.path.join(path))

                for _ in range(number_of_folders):
                    os.mkdir(path + '\\' + '.join(x for _ in range(length_of_folder_name) for x in _string.printable[(random.randint(0, 61))]))

                os.startfile('path')

            [EXPLANATION of CODE]
                Here, ''.join(x for _ in range(length_of_folder_name) for x in _string.printable[(random.randint(0, 61))])

                        first gets the random letters from string.printable by slicing with random number generated between (0, 61) by random.randint(0, 61)

                        and then the join function joins the every letter

                        '_' is throwaway variable

                        Example: Lets assume:
                                    length_of_folder_name = 10
                                    number_of_folder = 100

                                    The first loop "for _ in range(number_of_folders)" is used to make folder

                                    Then the for loop iterate for 10 times and generates random letter like (a,w,2,q,k,i,4,j,x,v) and the built in function
                                    joins them together and forms "aw2qki4jxv" for every loop in first loop'''


if __name__ == '__main__':
    hunderd_folders(100, 20)
