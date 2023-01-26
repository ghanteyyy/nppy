import os
import sys
import json
import random
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font
import pygame


class _Entry:
    def __init__(self, frame, StyleName, DefaultText):
        self.frame = frame
        self.IsDefault = True
        self.ErrorTimer = None
        self.DEFAULT_TEXT = DefaultText
        self.entry_style = StyleName + '.TEntry'

        self.var = StringVar()
        self.var.set(self.DEFAULT_TEXT)

        self.EntryStyle = ttk.Style()
        self.EntryStyle.configure(self.entry_style, foreground='grey')
        self.Entry = ttk.Entry(self.frame, width=40, textvariable=self.var, justify='center', style=self.entry_style)

        self.Entry.bind("<FocusIn>", self.focus_in)
        self.Entry.bind("<FocusOut>", self.focus_out)

    def focus_in(self, event=None):
        '''
        Remove temporary placeholder's text when user clicks to respective entry widget
        '''

        if self.IsDefault:
            self.var.set('')
            self.IsDefault = False
            self.EntryStyle.configure(self.entry_style, foreground='black')

    def focus_out(self, event=None):
        '''
        Remove temporary placeholder's text when user clicks out of
        respective entry widget
        '''

        if self.IsDefault is False and not self.var.get().strip():
            self.IsDefault = True
            self.var.set(self.DEFAULT_TEXT)
            self.EntryStyle.configure(self.entry_style, foreground='grey')

    def SetDefault(self):
        '''
        Set Entry values to default
        '''

        self.IsDefault = True
        self.var.set(self.DEFAULT_TEXT)
        self.EntryStyle.configure(self.entry_style, foreground='grey')


class Quiz:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.QuizNumbers = []
        self.IsInfoMessageShown = False
        self.FileName = os.path.abspath(os.path.join('.', 'quiz.json'))
        self.ButtonsAttributes = {'fg': 'white', 'activeforeground': 'white', 'cursor': 'hand2', 'bd': 0, 'width': 34}

        self.Window = Tk()

        if sys.platform == 'win32':
            self.ErrorAudio = self.ResourcePath('WinErrSound.wav')

        else:
            self.ErrorAudio = self.ResourcePath('LinuxErrSound.wav')

        pygame.mixer.music.load(self.ErrorAudio)

        self.TitleImage = PhotoImage(file=self.ResourcePath('title.png'))

        self.TitleLabel = Label(self.Window, image=self.TitleImage, bd=0, bg='white')
        self.TitleLabel.pack(ipadx=13)

        self.LabelFrame = Frame(self.Window, bg='white')
        self.LabelFrame.pack()

        self.AddLabelFrame = LabelFrame(self.LabelFrame, text='Add Q/A', bg='white')
        self.AddLabelFrame.pack(side=LEFT, padx=(10, 0), pady=10, ipadx=10, fill='y')

        self.QuestionEntry = _Entry(self.AddLabelFrame, 'Q', 'QUESTION')
        self.QuestionEntry.Entry.pack(pady=5, ipady=3)

        self.AnswerEntry = _Entry(self.AddLabelFrame, 'A', 'ANSWER')
        self.AnswerEntry.Entry.pack(pady=5, ipady=3)

        self.AddButton = Button(self.AddLabelFrame, text='ADD QUESTION', bg='red', activebackground='red', **self.ButtonsAttributes, command=self.AddButtonCommand)
        self.AddButton.pack(pady=5, ipady=5)

        self.PickLabelFrame = LabelFrame(self.LabelFrame, text='PICK QUESTION', bg='white')
        self.PickLabelFrame.pack(side=RIGHT, ipadx=10, padx=10, pady=10)

        self.PickQuestionEntry = _Entry(self.PickLabelFrame, 'QN', 'QUESTION NUMBER')
        self.PickQuestionEntry.Entry.pack(pady=5, ipady=5)

        self.PickButton = Button(self.PickLabelFrame, text='PICK', bg='green', activebackground='green', **self.ButtonsAttributes, command=self.ManualPickQuestion)
        self.PickButton.pack(pady=5, ipady=5)

        self.RandomPickButton = Button(self.PickLabelFrame, text='PICK RANDOM QUESTION', bg='blue', activebackground='blue', **self.ButtonsAttributes, command=self.PickRandomQuestion)
        self.RandomPickButton.pack(pady=5, ipady=5)

        self.RandomQuestionAnswerLabelVar = StringVar()
        self.RandomQuestionAnswerLabel = Label(self.Window, textvariable=self.RandomQuestionAnswerLabelVar, bg='white')

        self.Window.after(0, self.CenterWindow)
        self.Window.bind('<Control-n>', self.ShowNumbers)
        self.Window.bind('<Control-N>', self.ShowNumbers)
        self.Window.bind_all('<Button-1>', self.FocusToWidget)
        self.AddButton.bind('<Return>', self.AddButtonCommand)
        self.PickButton.bind('<Return>', self.ManualPickQuestion)
        self.AnswerEntry.Entry.bind('<Return>', self.AddButtonCommand)
        self.QuestionEntry.Entry.bind('<Return>', self.AddButtonCommand)
        self.RandomPickButton.bind('<Return>', self.ManualPickQuestion)
        self.PickQuestionEntry.Entry.bind('<Return>', self.ManualPickQuestion)

        self.Window.config(bg='white')
        self.Window.mainloop()

    def FocusToWidget(self, event=None):
        '''
        Focus to the clicked widget
        '''

        event.widget.focus()

    def CenterWindow(self):
        '''
        Setting initial position to the center of the screen
        '''

        self.Window.withdraw()
        self.Window.update()

        width, height = self.Window.winfo_width(), self.Window.winfo_height() + 5
        screen_width, screen_height = self.Window.winfo_screenwidth(), self.Window.winfo_screenheight()
        self.Window.geometry(f'+{screen_width // 2 - width // 2}+{screen_height // 2 - height // 2}')

        self.IconImage = PhotoImage(file=self.ResourcePath('icon.png'))
        self.Window.iconphoto(False, self.IconImage)

        self.Window.title('Quiz')

        self.Window.deiconify()
        self.Window.resizable(0, 0)

    def ReadJSON(self):
        '''
        Reading data from the .json file
        '''

        try:
            with open(self.FileName, 'r') as f:
                contents = json.load(f)

                if not contents:
                    contents = {}

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open(self.FileName, 'w'):
                contents = {}

        return contents

    def WriteJSON(self, contents):
        '''
        Storing data to the .json file
        '''

        with open(self.FileName, 'w') as f:
            json.dump(contents, f, indent=4)

    def AddButtonCommand(self, event=None):
        '''
        When user clicks add question button
        '''

        question = self.QuestionEntry.var.get().strip()
        answer = self.AnswerEntry.var.get().strip()

        if question in ['', 'QUESTION']:
            self.ShowInfoMessage('Provide a valid question', 'red')

        elif answer in ['', 'ANSWER']:
            self.ShowInfoMessage('Provide a valid answer', 'red')

        else:
            contents = self.ReadJSON()

            if contents:
                head = int(list(contents.keys())[-1]) + 1

            else:
                head = 1

            tail = {'QUESTION': question, 'ANSWER': answer}
            contents[head] = tail

            self.WriteJSON(contents)

            # Setting entry widgets to default
            self.Window.focus()
            self.QuestionEntry.SetDefault()
            self.AnswerEntry.SetDefault()

    def ShowInfoMessage(self, msg, color):
        '''
        Show Error message or Question-Answer information
        '''

        pygame.mixer.music.play()

        self.RandomQuestionAnswerLabelVar.set(msg)
        self.RandomQuestionAnswerLabel.pack(pady=10, fill='both')

        if self.IsInfoMessageShown:
            self.Window.after_cancel(self.ErrorTimer)
            self.ErrorTimer = None

        if color == 'red':
            self.IsInfoMessageShown = True
            self.RandomQuestionAnswerLabel.config(fg=color, font=font.Font(size=15, weight='bold'))
            self.ErrorTimer = self.Window.after(1500, self.RemoveInfoMessage)

        else:
            self.RandomQuestionAnswerLabel.config(fg=color, font=font.Font(size=15), justify='left')

    def RemoveInfoMessage(self):
        '''
        Remove Error message after 1.5 seconds
        '''

        self.IsInfoMessageShown = False
        self.RandomQuestionAnswerLabel.pack_forget()

    def ManualPickQuestion(self, event=None, QuestionNumber=None):
        '''
        Retrieve the question with respect to the question number provided by
        the user
        '''

        contents = self.ReadJSON()

        if not QuestionNumber:
            QuestionNumber = self.PickQuestionEntry.var.get().strip()

        if len(self.QuizNumbers) == len(contents.keys()):
            self.ShowInfoMessage('No more questions available', 'red')

        elif QuestionNumber in ['', 'QUESTION NUMBER']:
            self.ShowInfoMessage('Provide Valid QUESTION NUMBER', 'red')

        elif QuestionNumber not in contents:
            self.ShowInfoMessage('Question number does not exist', 'red')

        elif QuestionNumber in self.QuizNumbers:
            self.ShowInfoMessage('Question number is already taken', 'red')

        else:
            question = contents[QuestionNumber]['QUESTION']
            answer = contents[QuestionNumber]['ANSWER']
            self.ShowInfoMessage(f'{QuestionNumber}. {question}\n\n  Ans. {answer}', 'black')

            self.PickQuestionEntry.SetDefault()
            self.QuizNumbers.append(QuestionNumber)

            self.Window.focus()

    def PickRandomQuestion(self):
        '''
        Retrieve question randomly
        '''

        try:
            all_keys = [value for value in self.ReadJSON().keys() if value not in self.QuizNumbers]
            RandomKey = random.choice(all_keys)

            self.ManualPickQuestion(QuestionNumber=RandomKey)

        except IndexError:
            self.ShowInfoMessage('No more questions available', 'red')

    def ShowNumbers(self, event=None):
        '''
        Show available question numbers when user presses Control-N or
        Control-Shift-N
        '''

        numbers = [num for num in self.ReadJSON().keys() if num not in self.QuizNumbers]
        self.ShowInfoMessage(f'Valid Numbers: {", ".join(numbers)}', 'black')

    def ResourcePath(self, FileName):
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

        return os.path.join(base_path, 'assets', FileName)


if __name__ == '__main__':
    Quiz()
