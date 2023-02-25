import os
import sys
from tkinter import *
from tkinter.font import Font
import tkinter.ttk as ttk
import pygame
import pyperclip
from PIL import Image, ImageTk
from converter import NumberSystemConversion


class GUI:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        if sys.platform == 'win32':
            self.AudioFile = self.ResourcePath('WinErrSound.wav')

        else:
            self.AudioFile = self.ResourcePath('LinuxErrSound.wav')

        pygame.mixer.music.load(self.AudioFile)

        self.IsEntryDefault = True
        self.DefaultText = 'Enter Number'

        self.master = Tk()
        self.master.withdraw()
        self.master.title('Number System')
        self.master.iconbitmap(self.ResourcePath('icon.ico'))

        self.ImageFile = Image.open(self.ResourcePath('cover.jpg'))
        self.ImageFile.thumbnail((800, 800), Image.Resampling.LANCZOS)
        self.ImageFile = ImageTk.PhotoImage(self.ImageFile)

        self.Canvas = Canvas(self.master, highlightthickness=0)
        self.Canvas.pack(fill='both', expand=True)

        self.Canvas.create_image(0, 0, anchor='nw', image=self.ImageFile)

        self.ComboValues = ['Binary to Decimal', 'Binary to Octal', 'Binary to Hexadecimal', 'Binary to Quinary',
                            'Decimal to Binary', 'Decimal to Octal', 'Decimal to Hexadecimal', 'Decimal to Quinary',
                            'Octal to Binary', 'Octal to Decimal', 'Octal to Hexadecimal', 'Octal to Quinary',
                            'Hexadecimal to Binary', 'Hexadecimal to Decimal', 'Hexadecimal to Octal', 'Hexadecimal to Quinary',
                            'Quinary to Binary', 'Quinary to Decimal', 'Quinary to Octal', 'Quinary to Hexadecimal']

        self.EntryVar = StringVar()
        self.EntryStyle = ttk.Style()
        self.EntryStyle.configure('E.TEntry', foreground='grey')
        self.EntryBox = ttk.Entry(self.master, width=33, textvariable=self.EntryVar, justify='center', style='E.TEntry')
        self.EntryVar.set(self.DefaultText)

        self.ComboBox = ttk.Combobox(self.master, values=self.ComboValues, width=30, justify='center')
        self.ComboBox.set('Select Number System')

        self.ConvertButton = Button(self.master, width=28, height=2, fg='white', bg='Green', bd='0', activebackground='Green', activeforeground='white', text='CONVERT', cursor='hand2', command=self.calculation)

        self.Canvas.create_window(190, 80, window=self.EntryBox, height=28)
        self.Canvas.create_window(190, 115, window=self.ComboBox, height=28)
        self.Canvas.create_window(190, 154, window=self.ConvertButton)

        self.master.bind('<Return>', self.calculation)
        self.EntryBox.bind('<FocusIn>', self.FocusIn)
        self.EntryBox.bind('<FocusOut>', self.FocusOut)
        self.master.bind('<Button-1>', self.FocusAnyWhere)
        self.ComboBox.bind('<Button-1>', self.ComboSingleClick)

        self.InitialWindowPosition()
        self.master.mainloop()

    def InitialWindowPosition(self):
        '''
        Set window to center of the screen when it starts
        '''

        self.master.update()

        ScreenWidth = self.master.winfo_screenwidth() // 2
        ScreenHeight = self.master.winfo_screenheight() // 2

        width = self.master.winfo_reqwidth() // 2
        height =self.master.winfo_reqheight() // 2

        x = ScreenWidth - width
        y = ScreenHeight - height

        self.master.geometry(f'+{x}+{y}')
        self.master.resizable(0, 0)

        self.master.deiconify()

    def FocusAnyWhere(self, event=None):
        '''
        Set Focus to clicked widget
        '''

        event.widget.focus_set()

    def FocusIn(self, event=None):
        '''
        When users clicks to Entry Widget
        '''

        if self.IsEntryDefault:
            self.EntryVar.set('')
            self.IsEntryDefault = False
            self.EntryStyle.configure('E.TEntry', foreground='black')

    def FocusOut(self, event=None):
        '''
        When users clicks to Entry Widget
        '''

        if not self.EntryVar.get().strip():
            self.IsEntryDefault = True
            self.EntryVar.set(self.DefaultText)
            self.EntryStyle.configure('E.TEntry', foreground='grey')

    def ComboSingleClick(self, event=None):
        '''
        Show drop-down items when clicked to ComboBox
        '''

        self.ComboBox.event_generate('<Down>', when='head')

    def PlayErrorAudio(self):
        '''
        Play error audio
        '''

        pygame.mixer.music.play()

    def DisplayAnswer(self, result):
        '''
        Display answer or errors
        '''

        if 'valid' in result.lower():
            fg = 'red'

        else:
            fg = 'white'

        self.CanvasResultText = self.Canvas.create_text(200, 200, text=result, fill=fg, width=200, font=Font(size=15))

        if 'valid' not in result.lower():
            self.CopyToClipBoardButton = Button(self.master, text='Copy', bd=0, bg='dark green', activebackground='green', fg='white', activeforeground='white', command=lambda: self.CopyToClipBoard(text=result))
            self.CanvasCopyToClipBoardButton = self.Canvas.create_window(250, 240, window=self.CopyToClipBoardButton, height=40, width=70)
            self.CopyToClipBoardButton.bind('<Button-1>', lambda event=Event, text=result: self.CopyToClipBoard(event, text))

        else:
            self.master.after(2000, self.RemoveWidgets)

    def CopyToClipBoard(self, event=None, text=None):
        '''
        Copy obtained result to clipboard
        '''

        pyperclip.copy(text)

        self.CopyToClipBoardButton.config(text='Copied !!!')
        self.master.focus()

        self.master.after(2000, lambda: self.Canvas.delete(self.CanvasCopyToClipBoardButton))

    def RemoveWidgets(self):
        '''
        Remove the label and button displayed after obtaining the result
        '''

        try:
            self.Canvas.delete(self.CanvasResultText)
            self.Canvas.delete(self.CanvasCopyToClipBoardButton)

        except AttributeError:
            pass

    def calculation(self, event=None):
        '''
        Converting number with respective selected conversion
        '''

        self.RemoveWidgets()
        get_value = self.EntryVar.get().strip()

        if get_value == self.DefaultText or not get_value:
            self.PlayErrorAudio()
            answer = 'Input Valid Number'

        elif self.ComboBox.get() == 'Select Number System':
            self.PlayErrorAudio()
            answer = 'Select Valid Conversion'

        else:
            combo_get = self.ComboBox.get()
            number_system = NumberSystemConversion(self.DisplayAnswer, self.PlayErrorAudio)

            if combo_get == 'Binary to Decimal':
                answer = number_system.binary_to_decimal(get_value)

            elif combo_get == 'Binary to Octal':
                answer = number_system.binary_to_octal(get_value)

            elif combo_get == 'Binary to Hexadecimal':
                answer = number_system.binary_to_hexadecimal(get_value)

            elif combo_get == 'Binary to Quinary':
                answer = number_system.binary_to_quinary(get_value)

            elif combo_get == 'Decimal to Binary':
                answer = number_system.decimal_to_binary(get_value)

            elif combo_get == 'Decimal to Octal':
                answer = number_system.decimal_to_octal(get_value)

            elif combo_get == 'Decimal to Hexadecimal':
                answer = number_system.decimal_to_hexadecimal(get_value)

            elif combo_get == 'Decimal to Quinary':
                answer = number_system.decimal_to_quinary(get_value)

            elif combo_get == 'Octal to Binary':
                answer = number_system.octal_to_binary(get_value)

            elif combo_get == 'Octal to Decimal':
                answer = number_system.octal_to_decimal(get_value)

            elif combo_get == 'Octal to Hexadecimal':
                answer = number_system.octal_to_hexadecimal(get_value)

            elif combo_get == 'Octal to Quinary':
                answer = number_system.octal_to_quinary(get_value)

            elif combo_get == 'Hexadecimal to Binary':
                answer = number_system.hexadecimal_to_binary(get_value)

            elif combo_get == 'Hexadecimal to Decimal':
                answer = number_system.hexadecimal_to_decimal(get_value)

            elif combo_get == 'Hexadecimal to Octal':
                answer = number_system.hexadecimal_to_octal(get_value)

            elif combo_get == 'Hexadecimal to Quinary':
                answer = number_system.hexadecimal_to_quinary(get_value)

            elif combo_get == 'Quinary to Binary':
                answer = number_system.quinary_to_binary(get_value)

            elif combo_get == 'Quinary to Decimal':
                answer = number_system.quinary_to_decimal(get_value)

            elif combo_get == 'Quinary to Octal':
                answer = number_system.quinary_to_octal(get_value)

            elif combo_get == 'Quinary to Hexadecimal':
                answer = number_system.quinary_to_hexadecimal(get_value)

        if answer:
            self.DisplayAnswer(answer)

    def ResourcePath(self, file_name):
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


if __name__ == '__main__':
    GUI()
