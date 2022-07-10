import os
import sys
import json
import random
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox


class Quiz:
    def __init__(self):
        self.prev_widget = ''
        self.quiz_numbers = []
        self.file_name = os.path.abspath(os.path.join('.', 'quiz.json'))
        self.buttons_attributes = {'fg': 'white', 'activeforeground': 'white', 'cursor': 'hand2', 'relief': RIDGE}

        self.master = Tk()

        self.title_img_obj = PhotoImage(file=self.resource_path('title.png'))
        self.title_label = Label(self.master, image=self.title_img_obj, bd=0, bg='white')
        self.title_label.pack(ipadx=13)

        self.add_labelframe = LabelFrame(self.master, text='Add Q/A', bg='white')
        self.question_entry_style = ttk.Style()
        self.question_entry_style.configure('Q.TEntry', foreground='grey')
        self.question_entry = ttk.Entry(self.add_labelframe, width=40, justify='center', style='Q.TEntry')
        self.question_entry.insert(END, 'QUESTION')
        self.question_entry.pack(pady=5, ipady=3)

        self.answer_entry_style = ttk.Style()
        self.answer_entry_style.configure('A.TEntry', foreground='grey')
        self.answer_entry = ttk.Entry(self.add_labelframe, width=40, justify='center', style='A.TEntry')
        self.answer_entry.insert(END, 'ANSWER')
        self.answer_entry.pack(pady=5, ipady=3)

        self.add_button = Button(self.add_labelframe, text='ADD QUESTION', bg='red', activebackground='red', **self.buttons_attributes, command=self.add_button_command)
        self.add_button.pack(pady=5, ipady=3, ipadx=73)
        self.add_labelframe.pack(pady=10, ipadx=10)

        self.pick_labelframe = LabelFrame(self.master, text='PICK QUESTION', bg='white')
        self.pick_question_entry_style = ttk.Style()
        self.pick_question_entry_style.configure('QN.TEntry', foreground='grey')
        self.pick_question_entry = ttk.Entry(self.pick_labelframe, width=40, justify='center', style='QN.TEntry')
        self.pick_question_entry.insert(END, 'QUESTION NUMBER')
        self.pick_question_entry.pack(pady=5, ipady=3)

        self.pick_button = Button(self.pick_labelframe, text='PICK', bg='green', activebackground='green', **self.buttons_attributes, command=self.manual_pick_question)
        self.pick_button.pack(pady=5, ipady=3, ipadx=107)

        self.random_pick_button = Button(self.pick_labelframe, text='PICK RANDOM QUESTION', bg='blue', activebackground='blue', **self.buttons_attributes, command=self.random_pick_question)
        self.random_pick_button.pack(pady=5, ipady=3, ipadx=47)
        self.pick_labelframe.pack(ipadx=10)

        self.master.after(0, self.center_window)
        self.master.bind('<Control-n>', self.show_numbers)
        self.master.bind('<Control-N>', self.show_numbers)
        self.master.bind('<Button-1>', self.master_bindings)
        self.add_button.bind('<FocusIn>', self.entry_bindings)
        self.pick_button.bind('<FocusIn>', self.entry_bindings)
        self.answer_entry.bind('<FocusIn>', self.entry_bindings)
        self.add_button.bind('<Return>', self.add_button_command)
        self.question_entry.bind('<FocusIn>', self.entry_bindings)
        self.answer_entry.bind('<Return>', self.add_button_command)
        self.pick_button.bind('<Return>', self.manual_pick_question)
        self.question_entry.bind('<Return>', self.add_button_command)
        self.pick_question_entry.bind('<FocusIn>', self.entry_bindings)
        self.random_pick_button.bind('<Return>', self.manual_pick_question)
        self.pick_question_entry.bind('<Return>', self.manual_pick_question)

        self.master.config(bg='white')
        self.master.mainloop()

    def center_window(self):
        '''Setting initial position to the center of the screen'''

        self.master.withdraw()
        self.master.update()

        width, height = self.master.winfo_width(), self.master.winfo_height() + 5
        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')
        self.master.iconbitmap(self.resource_path('icon.ico'))
        self.master.title('Quiz')

        self.master.deiconify()
        self.master.resizable(0, 0)

    def master_bindings(self, event=None):
        '''When user clicks anywhere outside of entry boxes and buttons'''

        widget = event.widget
        widgets = [self.question_entry, self.answer_entry, self.pick_question_entry, self.add_button, self.pick_button, self.random_pick_button]
        entries_widgets = {self.question_entry: 'QUESTION', self.answer_entry: 'ANSWER', self.pick_question_entry: 'QUESTION NUMBER'}
        entries_styles = {self.question_entry: (self.question_entry_style, 'Q.TEntry'), self.answer_entry: (self.answer_entry_style, 'A.TEntry'),
                          self.pick_question_entry: (self.pick_question_entry_style, 'QN.TEntry')}

        for wid in entries_widgets:
            if not wid.get().strip() and widget != self.prev_widget:
                wid.delete(0, END)
                wid.insert(END, entries_widgets[wid])
                style, style_name = entries_styles[wid]
                style.configure(style_name, foreground='grey')

        if widget not in widgets:
            self.master.focus()

    def entry_bindings(self, event=None):
        '''When user clicks in or out of the entries widget'''

        widget = event.widget
        entries_widgets = {self.question_entry: 'QUESTION', self.answer_entry: 'ANSWER', self.pick_question_entry: 'QUESTION NUMBER'}
        entries_styles = {self.question_entry: (self.question_entry_style, 'Q.TEntry'), self.answer_entry: (self.answer_entry_style, 'A.TEntry'),
                          self.pick_question_entry: (self.pick_question_entry_style, 'QN.TEntry')}

        if widget in entries_widgets:
            if widget.get().strip() == entries_widgets[widget]:
                widget.delete(0, END)
                self.prev_widget = widget
                style, style_name = entries_styles[widget]
                style.configure(style_name, foreground='black')

                entries_widgets.pop(widget)
                entries_styles.pop(widget)

        for wid in entries_widgets:
            if not wid.get().strip():
                wid.delete(0, END)
                wid.insert(END, entries_widgets[wid])
                style, style_name = entries_styles[wid]
                style.configure(style_name, foreground='grey')

    def read_json(self):
        '''Reading data from the .json file.'''

        try:
            with open(self.file_name, 'r') as f:
                contents = json.load(f)

                if not contents:
                    contents = {}

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open(self.file_name, 'w'):
                contents = {}

        return contents

    def write_json(self, contents):
        '''Storing data to the .json file'''

        with open(self.file_name, 'w') as f:
            json.dump(contents, f, indent=4)

    def add_button_command(self, event=None):
        '''When user clicks add question button'''

        question = self.question_entry.get().strip()
        answer = self.answer_entry.get().strip()

        if question in ['', 'QUESTION']:
            messagebox.showerror('Invalid Entry', 'Provide a valid question')

        elif answer in ['', 'ANSWER']:
            messagebox.showerror('Invalid Entry', 'Provide a valid answer')

        else:
            contents = self.read_json()

            if contents:
                head = int(list(contents.keys())[-1]) + 1

            else:
                head = 1

            tail = {'QUESTION': question, 'ANSWER': answer}
            contents[head] = tail

            self.write_json(contents)

            # Setting entry widgets to default
            self.question_entry.focus()
            self.answer_entry.delete(0, END)
            self.question_entry.delete(0, END)
            self.answer_entry.insert(END, 'ANSWER')
            self.question_entry.insert(END, 'QUESTION')
            self.answer_entry_style.configure('A.TEntry', foreground='grey')
            self.question_entry_style.configure('Q.TEntry', foreground='grey')

    def manual_pick_question(self, event=None, question_number=None):
        '''Retrieve the question with respect to the question number provided by the user'''

        contents = self.read_json()

        if not question_number:
            question_number = self.pick_question_entry.get().strip()

        if len(self.quiz_numbers) == len(contents.keys()):
            messagebox.showinfo('No questions', 'No more questions available')

        elif question_number in ['', 'QUESTION NUMBER']:
            messagebox.showerror('Invalid Entry', 'Provide Valid QUESTION NUMBER')

        elif question_number not in contents:
            messagebox.showinfo('Not Found', 'Question number does not exist')

        elif question_number in self.quiz_numbers:
            messagebox.showinfo('Invalid Question Number', 'Question number is already taken')

        else:
            question = contents[question_number]['QUESTION']
            answer = contents[question_number]['ANSWER']
            messagebox.showinfo('Q/A', f'{question_number}. {question}\n\n  Ans. {answer}')

            self.pick_question_entry.delete(0, END)
            self.pick_question_entry.insert(END, 'QUESTION NUMBER')
            self.pick_question_entry_style.configure('QN.TEntry', foreground='grey')

            self.quiz_numbers.append(question_number)

            self.master.focus()

    def random_pick_question(self):
        '''Retrieve question randomly'''

        try:
            all_keys = [value for value in self.read_json().keys() if value not in self.quiz_numbers]
            random_key = random.choice(all_keys)

            self.manual_pick_question(question_number=random_key)

        except IndexError:
            messagebox.showinfo('No questions', 'No more questions available')

    def show_numbers(self, event=None):
        '''Show available question numbers when user presses control-s'''

        numbers = [num for num in self.read_json().keys() if num not in self.quiz_numbers]
        messagebox.showinfo('Valid Numbers', ', '.join(numbers))

    def resource_path(self, file_name):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    Quiz()
