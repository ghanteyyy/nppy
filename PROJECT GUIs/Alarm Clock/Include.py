import os
import sys
import json
import time


def UpdateTitle(win, title_prefix):
    '''
    Update window title with current time

    param:
        win: object of Tk or Toplevel instance
        title_prefix: window's title name
    '''

    curr_time = time.strftime("%I : %M : %S %p")
    title = f'{title_prefix} | {curr_time}'

    win.title(title)
    win.after(250, lambda: UpdateTitle(win, title_prefix))


def ReadJSON():
    '''
    Read the alarm file
    '''

    try:
        with open('Alarm.json', 'r') as f:
            contents = json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):
        contents = dict()

    return contents


def WriteToJson(contents):
    '''
    Save alarms details to the alarm file

    param:
        contents: dictionary object of the alarm that is to written in the json file
    '''

    with open('Alarm.json', 'w') as f:
        json.dump(contents, f, indent=4)


def ResourcePath(FileName):
    '''
    Get absolute path to resource from temporary directory

    In development:
        Gets path of files that are used in this script like icons, images or
        file of any extension from current directory

    After compiling to .exe with pyinstaller and using --add-data flag:
        Gets path of files that are used in this script like icons, images or
        file of any extension from temporary directory


    param:
        FileName: image, audio, or any other file_name present in the assets directory
    '''

    try:
        base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

    except AttributeError:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, 'assets', FileName)
