import os
import sys
import json

timer = None


def initial_position(master):
    '''Start the program in the center of the screen'''

    master.withdraw()
    master.update()

    master.iconbitmap(resource_path('included_files\\icon.ico'))
    master.title('Untitled - GPAD')

    width, height = master.winfo_width() + 348, master.winfo_height() + 60
    screen_width, screen_height = master.winfo_screenwidth() // 2, master.winfo_screenheight() // 2

    try:
        win_details = get_font_details()['window_dimension']

        if win_details:
            master.geometry(win_details)

        else:
            master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')

    except KeyError:
        master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')

    master.deiconify()


def resource_path(relative_path):
    '''Get absolute path to resource from temporary directory

    In development:
        Gets path of files that are used in this script like icons, images or file of any extension from current directory

    After compiling to .exe with pyinstaller and using --add-data flag:
        Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

    try:
        base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS.

    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_font_details():
    '''Get font-family, font-size and font-style from the json file'''

    try:
        with open('settings.json', 'r') as f:
            curr_font = json.load(f)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        curr_font = {'Font Family': 'Courier', 'Font Size': 9, 'Font Style': 'normal'}
        save_font_details(curr_font)

    return curr_font


def save_font_details(font_details):
    '''Saves font-family, font-size and font-style to the json file'''

    with open('settings.json', 'w') as f:
        json.dump(font_details, f, indent=4)


def config_font_style(font_style, font_obj):
    '''Configure font style to italic, bold, bold + italic and normal'''

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
    '''Config text to the status_label'''

    global timer

    try:
        master.after_cancel(timer)

    except ValueError:
        pass

    var.set(text)

    if time:
        timer = master.after(time, lambda: var.set(''))
