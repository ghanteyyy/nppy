import subprocess


def execute_command(command):
    '''Execute command from python that you would do directly from command prompt'''

    try:
        if not str(command).isalpha():
            command = str(command)

        subprocess.call('{}'.format(command), creationflags=0x08000000)

    except NameError:
        print('Invalid Command')


if __name__ == '__main__':
    execute_command('cls')
