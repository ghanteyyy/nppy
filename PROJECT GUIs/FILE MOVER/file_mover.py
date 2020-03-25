import os
import shutil
import winsound
import threading
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox


class move_or_copy:
    def __init__(self, from_path, to_path, file_type, var):
        self.var = var
        self.file_type = file_type
        self.from_path = from_path
        self.to_path = os.path.join(to_path, os.path.split(self.from_path)[1])
        self.files = [os.path.join(self.from_path, f) for f in os.listdir(self.from_path)]
        self.extensions_list = {'Text File': ['txt'],
                                'Audio': ['wav', 'aiff', 'mp3'],
                                'Programs': ['exe'],
                                'Image': ['tif', 'jpg', 'png', 'gif', 'jpeg'],
                                'MS-Office': ['doc', 'docx', 'docm', 'dotx', 'dotm', 'xlsx', 'xlsm', 'xltx', 'xltm', 'xlsb', 'xlam', 'pptx', 'pptm', 'potx', 'potm', 'ppam', 'ppsx', 'ppsm', 'sldx', 'sldm', 'thmx'],
                                'Video': ['mp4', 'm4a', 'm4v', 'f4v', 'f4a', 'm4b', 'm4r', 'f4b', 'mov', '3gp', '3gp2', '3g2', '3gpp', '3gpp2', 'ogg', 'oga', 'ogv', 'ogx', 'wmv', 'wma', 'asf', 'webm', 'flv', 'avi']}

        if self.file_type == 'ALL':
            self.extensions = [ext for k, v in self.extensions_list.items() for ext in v]

        elif self.file_type == 'Folders':
            self.extensions = 'Folders'

        else:
            self.extensions = self.extensions_list[self.file_type]

    def already_exists(self):
        '''Checking duplicates files of from_path and to_path'''

        global common_files

        if not os.path.exists(self.to_path):
            return False

        prev_files = set(os.listdir(self.from_path))
        pres_files = set(os.listdir(self.to_path))
        common_files = set([os.path.join(self.from_path, f) for f in prev_files & pres_files])

        if common_files:
            return True

        return False

    def filter_function(self, file):
        '''Filtering files as per the extension given by the user'''

        if os.path.isfile(file) and os.path.basename(file).split('.')[1].lower() in self.extensions:
            return True

        elif os.path.isdir(file) and self.extensions == 'Folders':
            return True

        return False

    def action(self, file=None):
        '''Copy or Move the files / folders'''

        to_path = os.path.join(self.to_path, os.path.basename(file))

        if os.path.isdir(file):
            if self.var == 2:
                shutil.move(file, to_path)

            else:
                shutil.copytree(file, to_path)

        else:
            if self.var == 2:
                shutil.move(file, to_path)

            else:
                shutil.copy(file, to_path)

    def main(self):
        '''Main function for copying and moving file / folders'''

        self.files = set(filter(self.filter_function, self.files))

        if self.file_type == 'ALL':
            self.folders = {os.path.join(self.from_path, dirs) for dirs in os.listdir(self.from_path)}
            self.files.update(self.folders)

        try:
            if self.already_exists():
                if not messagebox.askyesno('File Already Exists', 'Some files are already exists. Do you want to overwrite the files?'):
                    self.files = self.files - common_files

            for file in self.files:
                self.action(file)

            messagebox.showinfo('Operation Successful', 'Your operation is successfully completed')
            os.startfile(self.to_path)

        except FileExistsError:
            messagebox.showerror('Directory Already Exists', 'Please! Give new directory name')

        except FileNotFoundError:
            os.makedirs(self.to_path)
            self.main()


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.screen_width, self.screen_height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry(f'543x267+{self.screen_width // 2 - 543 // 2}+{self.screen_height // 2 - 267 // 2}')
        self.master.resizable(0, 0)
        self.font = ('Courier', 15, 'bold')
        self.master.title('File MOVER')
        self.master.iconbitmap('included files/icon.ico')

        self.title_label = Label(self.master, text='File MOVER', fg='white', background='green', font=('Times New Roman', 30, 'bold'))
        self.title_label.pack(fill='both', pady=11)

        self.copy_from_entry = Entry(self.master, fg='grey', font=self.font, width=40, justify='center', relief=GROOVE)
        self.copy_from_entry.insert(END, 'From Path')
        self.copy_from_entry.place(x=30, y=80)

        self.copy_to_entry = Entry(self.master, fg='grey', font=self.font, width=40, justify='center', relief=GROOVE)
        self.copy_to_entry.insert(END, 'To Path')
        self.copy_to_entry.place(x=30, y=130)

        self.combo_box = ttk.Combobox(self.master, value=['ALL', 'Image', 'Video', 'Audio', 'Folders', 'Programs', 'MS-Office', 'Text File'], width=23, height=4)
        self.combo_box.set('Select file types')
        self.combo_box.place(x=100, y=175)

        self.var = IntVar()
        self.copy_or_move_frame = Frame(self.master)
        self.copy_radio_button = Radiobutton(self.copy_or_move_frame, text='COPY', value=1, variable=self.var, bg='green', activebackground='green', fg='black', font=self.font)
        self.move_radio_button = Radiobutton(self.copy_or_move_frame, text='MOVE', value=2, variable=self.var, bg='green', activebackground='green', fg='black', font=self.font)
        self.copy_radio_button.grid(row=0, column=0)
        self.move_radio_button.grid(row=0, column=1)
        self.copy_or_move_frame.place(x=300, y=170)

        self.do_it_button_frame = Frame(self.master)
        self.do_it_button = Button(self.do_it_button_frame, text='Move / Copy', command=self.button_command, fg='white', bg='green', activebackground='green', activeforeground='white', relief=GROOVE, cursor='hand2')
        self.do_it_button.grid(row=0, column=0, ipadx=35, ipady=10)
        self.do_it_button_frame.place(x=200, y=210)

        self.copy_from_entry.bind('<Button-1>', lambda e: self.button_1_command(self.copy_from_entry, 'From Path'))
        self.copy_from_entry.bind('<Leave>', lambda e: self.leave(self.copy_from_entry, 'From Path'))

        self.copy_to_entry.bind('<Button-1>', lambda e: self.button_1_command(self.copy_to_entry, 'To Path'))
        self.copy_to_entry.bind('<Leave>', lambda e: self.leave(self.copy_to_entry, 'To Path'))

        self.master.config(bg='green')

    def button_1_command(self, widget, value):
        '''Activates when user clicks to the entry boxes'''

        widget.focus()

        if widget.get() == value:
            widget.delete(0, END)
            widget.config(fg='black')

    def leave(self, widget, value):
        '''Activates when user leaves the entry boxes'''

        if not widget.get().strip():
            self.master.focus()
            widget.delete(0, END)
            widget.insert(END, value)
            widget.config(fg='grey')

    def button_command(self):
        '''Activates when "Move / Copy" button is pressed'''

        from_path = self.copy_from_entry.get()
        to_path = self.copy_to_entry.get()
        combo_get = self.combo_box.get()
        var = self.var.get()

        if from_path == 'From Path' or to_path == 'To Path' or combo_get == 'Select file types' or var not in [1, 2]:
            winsound.MessageBeep()
            messagebox.showerror('Invalid Input', 'Some field(s) are left empty')

        else:
            moc = move_or_copy(from_path, to_path, combo_get, var)
            thread = threading.Thread(target=moc.main)
            thread.start()


if __name__ == '__main__':
    root = Tk()
    GUI(root)
    root.mainloop()
