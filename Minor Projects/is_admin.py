import sys
import ctypes


def is_admin():
    '''Execute your program with administrator privilege'''

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()

    except:
        return False


if is_admin():
    # Code of your program here
    pass


else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)


if __name__ == '__main__':
    is_admin()
