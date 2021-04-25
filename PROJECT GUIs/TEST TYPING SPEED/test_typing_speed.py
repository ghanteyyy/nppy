import os
import sys
import random
import string
from tkinter import *
import tkinter.ttk as ttk
from tkinter import PhotoImage, font


class Test_Typing_Speed:
    def __init__(self):
        self.time = 60
        self.running = False
        self.correct_words = 0
        self.total_keywords = 0
        self.incorrect_words = 0
        self.backspace_counter = 0
        self.correct_keystrokes = 0
        self.incorrect_keystrokes = 0

        self.prev_index = '1.0'
        self.redo_path = self.resource_path('included_files\\redo.png')
        self.icon_path = self.resource_path('included_files\\icon.ico')
        self.file_path = self.resource_path('included_files\\words.txt')

        with open(self.file_path, 'r') as f:
            self.contents = f.read().split()

        self.master = Tk()

        self.show_words = Text(self.master, width=40, height=1, font=font.Font(size=20), wrap='word', cursor='arrow')
        self.show_words.pack()

        self.typing_area_frame = Frame(self.master)
        self.typing_area_var = StringVar()
        self.typing_area = ttk.Entry(self.typing_area_frame, textvariable=self.typing_area_var, width=30, font=font.Font(size=15))
        self.typing_area.pack(side=LEFT, ipady=4)
        self.typing_area.focus_set()

        self.time_label_var = StringVar()
        self.time_label_var.set('01:00')
        self.time_label = Label(self.typing_area_frame, textvariable=self.time_label_var, font=font.Font(size=15), relief=SOLID)
        self.time_label.pack(side=LEFT, ipadx=1, ipady=4, padx=10)

        self.image_obj = PhotoImage(file=self.redo_path)
        self.redo_button = Button(self.typing_area_frame, image=self.image_obj, relief=GROOVE, command=self.redo)
        self.redo_button.pack(side=LEFT)
        self.typing_area_frame.pack(pady=5)

        self.insert_to_text_widget()
        self.initial_position()

        self.typing_area.bind('<F5>', self.redo)
        self.typing_area.bind('<space>', self.next_word)
        self.typing_area.bind('<BackSpace>', self.backspace)
        self.typing_area.bind('<KeyPress>', self.key_pressed)
        self.show_words.bind('<Enter>', self.forbid_default_bindings)
        self.show_words.bind('<Leave>', self.forbid_default_bindings)
        self.show_words.bind('<Motion>', self.forbid_default_bindings)
        self.show_words.bind('<MouseWheel>', self.forbid_default_bindings)
        self.typing_area.bind('<KeyRelease>', self.forbid_default_bindings)
        self.show_words.bind('<Double-Button-1>', self.forbid_default_bindings)

        self.master.mainloop()

    def initial_position(self):
        '''Set position of the window when opened for the first time'''

        self.master.withdraw()
        self.master.update()

        width, height = self.master.winfo_width(), self.master.winfo_height()
        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'+{screen_width - width // 2}+{screen_height - height // 2}')
        self.master.iconbitmap(self.icon_path)
        self.master.title('Test Typing Speed')

        self.master.deiconify()
        self.master.resizable(0, 0)

        self.show_words.focus()

    def key_pressed(self, event=None):
        '''When user presses any key which is printable'''

        value = event.keysym

        if value in string.printable:
            var_get = self.typing_area_var.get() + value
            selected_value = self.show_words.get('select.first', 'select.last')
            self.typing_area_var.set(var_get)
            self.typing_area.icursor('end')

            if selected_value.startswith(var_get):
                self.select_word()

            else:
                self.select_word('red')

            if self.running is False:
                self.running = True
                self.master.after(1000, self.track_time)

            return 'break'

    def backspace(self, event=None):
        '''When backspace key is pressed'''

        self.backspace_counter += 1
        var_get = self.typing_area_var.get()
        selected_value = self.show_words.get('select.first', 'select.last')

        if var_get:
            self.typing_area_var.set(var_get[:-1])

            if selected_value.startswith(var_get[:-1]):
                self.select_word()

            else:
                self.select_word('red')

            self.typing_area.icursor(len(var_get) - 1)

        return 'break'

    def forbid_default_bindings(self, event=None):
        '''Stop tkinter to execute its default bindings'''

        return 'break'

    def insert_to_text_widget(self):
        '''Insert random word from text-file when program opened for the
           first time or when redo button is clicked or F5 button is pressed'''

        random_words = ''
        self.show_words.config(state='normal')
        self.show_words.delete('1.0', 'end')

        for _ in range(220):
            text = random.choice(self.contents)

            if text == 'i':
                random_words += f'{text.upper()} '

            elif random.randint(0, 100) in range(20, 30):  # Make the first letter of the word capital when the random value is between 20-30. This is my preferences.
                random_words += f'{text.title()} '

            else:
                random_words += f'{text} '

        self.show_words.insert('1.0', random_words)  # Inserting the random value to the text-widget
        self.show_words.config(state='disabled')
        self.get_space_index()
        self.master.after(10, self.select_word)

    def get_space_index(self):
        '''Getting index of space key present in text-widget to select word when user clicks space-bar'''

        self.space_index = []

        start_pos = '1.0'

        while True:
            start_pos = self.show_words.search(' ', start_pos, END)

            if not start_pos:
                return self.space_index

            end_pos = f'{start_pos}+1c'
            self.space_index.append(start_pos)
            start_pos = end_pos

    def select_word(self, color='#dddddd', tag='select'):
        '''Set background color to green if user types correct word else set red background color'''

        if tag == 'select':
            self.show_words.tag_delete(tag)

        self.show_words.tag_add(tag, self.prev_index, self.space_index[0])
        self.show_words.tag_config(tag, background=color)

    def next_word(self, event=None):
        '''Select another word when user presses space-bar'''

        if self.running is False:
            self.running = True
            self.track_time()

        get_value = self.typing_area_var.get().strip()
        selected_value = self.show_words.get('select.first', 'select.last')
        len_selected_value = len(selected_value)

        self.total_keywords += len_selected_value

        if get_value == selected_value:  # When user typed word and selected word are same
            self.correct_words += 1
            self.correct_keystrokes += len_selected_value

        elif get_value != selected_value:  # When user typed word and selected word are not same
            self.incorrect_words += 1
            self.select_word('red', 'incorrect')
            self.incorrect_keystrokes += len_selected_value

        self.prev_index = f'{self.space_index[0]}+1c'
        self.space_index.pop(0)
        self.select_word()

        self.typing_area_var.set('')
        self.show_words.see(self.space_index[0])

        return 'break'

    def track_time(self, event=None):
        '''Decrease time by 1 second until it reaches 0'''

        if self.running is False:  # Stop timer when redo button is clicked
            if self.timer:
                self.master.after_cancel(self.timer)

        elif self.time > 0:  # Decrease time by 1 second and call this function again and again until time reaches to 0
            self.time -= 1
            self.time_label_var.set(f'00:{str(self.time).zfill(2)}')
            self.timer = self.master.after(1000, self.track_time)

        else:  # When time reaches to 0
            self.show_words.pack_forget()

            try:  # Calculating WPM
                gross_wpm = int(round(self.correct_keystrokes / 5, 0))
                accuracy = round((self.correct_keystrokes - self.incorrect_keystrokes - self.backspace_counter) / self.total_keywords * 100, 2)

                if accuracy < 0:
                    accuracy = 0

            except ZeroDivisionError:
                gross_wpm = accuracy = 0

            self.typing_area_var.set('')

            self.output_frame = Frame(self.master)

            # Display result
            wpm_frame = Frame(self.output_frame)
            wpm_label = Label(wpm_frame, text=f'{gross_wpm} WPM', fg='green', font=font.Font(size=20, weight='bold'))
            wpm_label.grid(row=0, column=0, sticky='w')

            full_from_label = Label(wpm_frame, text='(word per minute)', font=font.Font(size=13, weight='bold'))
            full_from_label.grid(row=0, column=1, sticky='w')
            wpm_frame.grid(row=0, column=0, sticky='w')

            text_1 = f'{"Keystrokes".ljust(20)}({self.correct_keystrokes} | {self.incorrect_keystrokes}) {self.total_keywords}\n'
            text_2 = f'{"Accuracy".ljust(20)}{accuracy} %\n'
            text_3 = f'{"Correct Words".ljust(20)}{self.correct_words}\n'
            text_4 = f'{"Wrong Words".ljust(20)}{self.incorrect_words}'

            text_widget = Text(self.output_frame, height=5, width=50, bg='#f0f0f0', border=0, cursor='arrow')
            text_widget.insert('1.0', f'{text_1}{text_2}{text_3}{text_4}')

            pip_index = text_widget.search("|", "1.21", "1.end")
            text_widget.tag_add('correct', '1.21', f'{pip_index}-1c')
            text_widget.tag_config('correct', foreground='green', font=font.Font(weight='bold', size=9))
            text_widget.tag_add('incorrect', f"{pip_index}+2c", text_widget.search(')', pip_index, '1.end'))
            text_widget.tag_config('incorrect', foreground='red', font=font.Font(weight='bold', size=9))
            text_widget.tag_add('corrcet_word', '3.20', '3.end')
            text_widget.tag_config('corrcet_word', foreground='green', font=font.Font(weight='bold'))
            text_widget.tag_add('incorrcet_word', '4.20', '4.end')
            text_widget.tag_config('incorrcet_word', foreground='red', font=font.Font(weight='bold'))

            text_widget.config(state='disabled')
            text_widget.grid(row=1, column=0)

            text_widget.bind('<Enter>', self.forbid_default_bindings)
            text_widget.bind('<Leave>', self.forbid_default_bindings)
            text_widget.bind('<Motion>', self.forbid_default_bindings)
            text_widget.bind('<Double-Button-1>', self.forbid_default_bindings)
            self.output_frame.pack()

    def redo(self, event=None):
        '''Reset everything to the beginning'''

        self.time = 60
        self.running = False
        self.prev_index = '1.0'
        self.typing_area_var.set('')
        self.time_label_var.set('00:00')

        self.total_keywords = 0
        self.correct_words = 0
        self.incorrect_words = 0
        self.backspace_counter = 0
        self.correct_keystrokes = 0
        self.incorrect_keystrokes = 0

        try:
            self.output_frame.destroy()
            self.typing_area_frame.pack_forget()

            self.show_words.pack()
            self.typing_area_frame.pack(pady=5)

        except AttributeError:
            pass

        self.master.after(5, self.insert_to_text_widget)

    def resource_path(self, relative_path):
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


if __name__ == '__main__':
    Test_Typing_Speed()
