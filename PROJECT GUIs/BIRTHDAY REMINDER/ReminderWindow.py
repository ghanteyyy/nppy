import os
import sys
import json
import time
from tkinter import *
from tkinter.font import Font
import pygame
from PIL import Image, ImageTk


class ReminderWindow:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.AudioFile = self.ResourcePath('tone.wav')
        self.TemplateImage = self.ResourcePath('template.jpg')
        self.FILE = os.path.abspath(os.path.join('.', 'data.json'))
        self.QuitButtonImage = self.ResourcePath('QuitButtonImage.png')

        pygame.mixer.music.load(self.AudioFile)

    def ResizeImages(self, person_image_path):
        '''
        Resize required images to appropriate sizes
        '''

        self.img = Image.open(self.TemplateImage)
        self.img.thumbnail((600, 600), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)

        self.PersonImage = Image.open(person_image_path)
        self.PersonImage.thumbnail((200, 200), Image.Resampling.LANCZOS)
        self.PersonImage = ImageTk.PhotoImage(self.PersonImage)

        self.QuitImage = Image.open(self.QuitButtonImage)
        self.QuitImage.thumbnail((250, 250))
        self.QuitImage = ImageTk.PhotoImage(self.QuitImage)

    def Window(self, _id, name, date, image):
        '''
        GUI window for showing wishes of those whose have birthday today
        '''

        _name = name.replace(' ', '\n')

        self.master = Tk()
        self.master.withdraw()
        self.master.resizable(0, 0)
        self.master.overrideredirect(True)
        self.master.title('BIRTHDAY REMINDER')
        self.master.wm_attributes('-topmost', 1)
        _font = Font(family='Segoe print', size=15, weight='bold')

        self.ResizeImages(image)

        self.BackgroundImage = Label(self.master, image=self.img)
        self.BackgroundImage.pack()

        self.PersonImageLabel = Label(self.master, image=self.PersonImage, bd=0)
        self.NameLabel = Label(self.master, bg='#d2f0fa', text=_name, font=_font)
        self.DateLabel = Label(self.master, bg='#c8ecfa', text=date, font=_font)
        self.CloseButton = Button(self.master, bg='#c20c06', activebackground='#c20c06', bd=0, cursor='hand2', image=self.QuitImage, command=lambda: self.QuitButtonCommand(_id))

        self.WindowPosition()
        self.master.mainloop()

    def WindowPosition(self):
        '''
        Set window position to the center of the screen when it starts
        '''

        self.master.update()

        width = self.master.winfo_width()
        height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth()

        self.master.geometry(f'+{screen_width - width}+0')

        self.CloseButton.place(x=width // 2 - 252 // 2.3, y=height - 65)
        self.PersonImageLabel.place(x=width // 2 - 163 // 2, y=height // 2 - 200 // 2)

        # Placing Name and Date Label to the top most part of the window so
        # that we can get the exact width and height of the respective label
        self.NameLabel.place(x=0, y=0)
        self.DateLabel.place(x=0, y=0)

        self.master.update()
        self.NameLabel.place(x=self.PersonImageLabel.winfo_x()- self.NameLabel.winfo_width(), y=self.PersonImageLabel.winfo_y() + self.PersonImageLabel.winfo_height() // 2 - self.NameLabel.winfo_height() // 2)
        self.DateLabel.place(x=self.PersonImageLabel.winfo_x() + self.PersonImageLabel.winfo_width(), y=self.PersonImageLabel.winfo_y() + self.PersonImageLabel.winfo_height() // 2 - self.DateLabel.winfo_height() // 2)

        pygame.mixer.music.play(-1)
        self.master.deiconify()

    def ChangeHasSeen(self):
        '''
        Set has_seen to false if it is already true. If true then it means that
        the birthday of the respective name has already been showed.
        '''

        from_file = self.ReadJSON()
        curr_time = time.strftime('%m-%d')

        for _, value in from_file.items():
            if value['has_seen'] and curr_time != value['date']:
                value['has_seen'] = False
                self.WriteJSON(from_file)

    def GetTodayBirthdaysDetails(self):
        '''
        Getting name, date and image of those whose birthday is today
        '''

        today_birth_dates = []
        from_file = self.ReadJSON()
        today_date = time.strftime('%m-%d')

        for _id, value in from_file.items():
            if value['has_seen'] is False and value['date'] == today_date:
                data = (_id, value['name'], value['date'], value['image'])
                today_birth_dates.append(data)

        return today_birth_dates

    def QuitButtonCommand(self, _id):
        '''
        Command when close button is closed

        When close button is clicked then set the has_seen to True so that the
        same birthday don't get displayed repeatedly
        '''

        pygame.mixer.music.stop()
        from_file = self.ReadJSON()

        for ID, value in from_file.items():
            if _id == ID:
                value['has_seen'] = True
                self.WriteJSON(from_file)
                break

        self.master.destroy()

    def ReadJSON(self):
        '''
        Reading data from the .json file
        '''

        try:
            with open(self.FILE, 'r') as f:
                contents = json.load(f)

        except FileNotFoundError:
            with open(self.FILE, 'w'):
                contents = {}

        except json.decoder.JSONDecodeError:
            contents = {}

        return contents

    def WriteJSON(self, contents):
        '''
        Storing data to the .json file
        '''

        with open(self.FILE, 'w') as f:
            json.dump(contents, f, indent=4)

    def main(self):
        '''
        Entry of the program
        '''

        while True:
            self.ChangeHasSeen()
            birth_dates = self.GetTodayBirthdaysDetails()

            for _id, name, date, image in birth_dates:
                self.Window(_id, name, date, image)

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
    reminder = ReminderWindow()
    reminder.main()
