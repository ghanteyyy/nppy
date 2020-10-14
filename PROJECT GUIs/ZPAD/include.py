import os
import sys
import json
import ctypes


def initial_position(master):
    '''Start the program in the center of the screen'''

    master.withdraw()
    master.update()

    master.iconbitmap(resource_path('included_files\\icon.ico'))
    master.title('Untitled - ZPAD')

    # width, height = 1007, 485
    width, height = master.winfo_width() + 348, master.winfo_height() + 60
    screen_width, screen_height = master.winfo_screenwidth() // 2, master.winfo_screenheight() // 2

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


class hide_or_show_maximize_minimize:
    '''Hide the minimize and maximize buton when the window is place at the top of other applications windows.
       And show the minimize and maximize button when the window is not place at the top of other applications windows'''

    def __init__(self, window):
        self.window = window

        # shortcuts to the WinAPI functionality
        self.set_window_pos = ctypes.windll.user32.SetWindowPos
        self.set_window_long = ctypes.windll.user32.SetWindowLongW
        self.get_window_long = ctypes.windll.user32.GetWindowLongW
        self.get_parent = ctypes.windll.user32.GetParent

        # some of the WinAPI flags
        self.SWP_NOSIZE = 1
        self.SWP_NOMOVE = 2
        self.GWL_STYLE = -16
        self.SWP_NOZORDER = 4
        self.SWP_FRAMECHANGED = 32
        self.WS_MAXIMIZEBOX = 65536
        self.WS_MINIMIZEBOX = 131072

    def hide_minimize_maximize(self):
        '''Hide minimize and maximize button of the window'''

        hwnd = self.get_parent(self.window.winfo_id())
        old_style = self.get_window_long(hwnd, self.GWL_STYLE)  # getting the old style
        new_style = old_style & ~ self.WS_MAXIMIZEBOX & ~ self.WS_MINIMIZEBOX  # building the new style (old style AND NOT Maximize AND NOT Minimize)
        self.set_window_long(hwnd, self.GWL_STYLE, new_style)  # setting new style
        self.set_window_pos(hwnd, 0, 0, 0, 0, 0, self.SWP_NOMOVE | self.SWP_NOSIZE | self.SWP_NOZORDER | self.SWP_FRAMECHANGED)  # updating non-client area


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
