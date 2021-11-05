import sys
import ctypes


def IsAdmin():
    '''Execute your program with administrator privilege'''

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()

    except:
        return False


if IsAdmin():
    # Code of your program here
    pass


else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, __file__, None, 1)


if __name__ == '__main__':
    IsAdmin()
