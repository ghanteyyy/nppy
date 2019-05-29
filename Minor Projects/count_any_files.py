import os

try:
    import win32con
    import win32file

except (NameError, ImportError, ModuleNotFoundError):
    print('pywin32 is not installed\nOR\nString was expected')


def count_any_files(drive, extension):
    '''Count number of files of given extension available in your drive'''

    counter = 0
    exclude = ['$RECYCLE.BIN', '$Recycle.Bin', '$SysReset', 'Config.Msi', 'Documents and Settings', 'ESD', 'hiberfil.sys', 'Intel', 'MSOCache', 'OneDriveTemp',
               'pagefile.sys', 'PerfLogs', 'Program Files', 'Program Files (x86)', 'ProgramData', 'Python27', 'Recovery', 'swapfile.sys', 'System Volume Information',
               'Windows', 'Public', '.idlerc', 'AppData', 'MicrosoftEdgeBackups', 'All Users']   # These directories is to be excluded. Add if you want other too

    drive_types = (win32con.DRIVE_REMOVABLE,)  # Removable disk type

    try:
        if win32file.GetDriveType(drive) in drive_types:  # Check if the the listed drive is removeable
            print('{} is removeable drive. Do not remove it until this process completes'.format(drive))

        for dirs, dirn, files in os.walk(drive):  # Walking through all directories and files of a given drive
            for di in dirn:
                if di in exclude:
                    dirn.remove(di)  # Removing directory if they are in exclude list

            for f in files:
                if f.endswith(extension):  # Checking if the obtained file's name end with given extension
                    counter += 1

        print('{}{}\n{}{}'.format('Drive'.ljust(15), 'Number of {} files'.format(extension).rjust(15), drive.rjust(4), str(counter).rjust(23)))

    except WindowsError as err:
        if err.strerror == 'The device is not ready':
            print('{} is not ready to use'.format(drive))

        if err.strerror == 'This drive is locked by BitLocker Drive Encryption. You must unlock this drive from Control Panel':
            print('{} is locked by BitLocker Drive Encryption. You must unlock this drive from Control Panel'.format(drive))


if __name__ == '__main__':
    count_any_files('D:\\', '.jpg')
