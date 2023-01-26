import os
import sys
import json

timer = None


def initial_position(master, text_widget):
    '''
    Start the program in the center of the screen
    '''

    master.withdraw()
    master.update()

    master.iconbitmap(resource_path('icon.ico'))
    master.title('Untitled - GPAD')

    master.state('zoomed')

    master.deiconify()
    text_widget.focus()


def resource_path(file_name):
    '''
    Get absolute path to resource from temporary directory

    In development:
        Gets path of files that are used in this script like icons, images or
        file of any extension from current directory

    After compiling to .exe with pyinstaller and using --add-data flag:
        Gets path of files that are used in this script like icons, images or
        file of any extension from temporary directory
    '''

    try:
        base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

    except AttributeError:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, 'assets', file_name)


def GetFontDetails():
    '''
    Get font-family, font-size and font-style from the json file
    '''

    DefaultValues = {
        'Font Family': 'Courier',
        'Font Size': 9,
        'Font Style': 'normal',
        'Number of Windows': 0,
        'Master Withdrawn': False
    }

    try:
        with open(resource_path('settings.json'), 'r') as f:
            curr_font = json.load(f)

            for key, value in DefaultValues.items():
                if key not in curr_font:
                    curr_font[key] = value

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        curr_font = DefaultValues

    SaveFontDetails(curr_font)

    return curr_font


def SaveFontDetails(font_details):
    '''
    Saves font-family, font-size and font-style to the json file
    '''

    with open(resource_path('settings.json'), 'w') as f:
        json.dump(font_details, f, indent=4)


def ConfigFontStyle(font_style, font_obj):
    '''
    Configure font style to italic, bold, bold + italic and normal
    '''

    if 'bold' in font_style:
        font_obj.configure(weight='bold')

    if 'italic' in font_style:
        font_obj.configure(slant='italic')

    if 'underline' in font_style:
        font_obj.configure(underline=1)

    if 'overstrike' in font_style:
        font_obj.configure(overstrike=1)

    if 'bold' not in font_style:
        font_obj.configure(weight='normal')

    if 'italic' not in font_style:
        font_obj.configure(slant='roman')

    if 'underline' not in font_style:
        font_obj.configure(underline=0)

    if 'overstrike' not in font_style:
        font_obj.configure(overstrike=0)


def set_var(master, var, text, time):
    '''
    Config text to the status_label
    '''

    global timer

    try:
        master.after_cancel(timer)

    except ValueError:
        pass

    var.set(text)

    if time:
        timer = master.after(time, lambda: var.set(''))
