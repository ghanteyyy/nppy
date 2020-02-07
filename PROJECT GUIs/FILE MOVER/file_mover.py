import os
import shutil
import winsound
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox


class move_or_copy:
    def __init__(self, from_path, to_path, file_type, var):
        self.from_path, self.var = from_path, var
        self.to_path = os.path.join(to_path, os.path.split(self.from_path)[1])
        self.files = [os.path.join(self.from_path, f) for f in os.listdir(self.from_path)]
        self.extension = {'Text File': 'txt',
                          'Audio': ['wav', 'aiff', 'mp3'],
                          'Image': ['tif', 'jpg', 'png', 'gif', 'jpeg'],
                          'MS-Office': ['doc', 'docx', 'docm', 'dotx', 'dotm', 'xlsx', 'xlsm', 'xltx', 'xltm', 'xlsb', 'xlam', 'pptx', 'pptm', 'potx', 'potm', 'ppam', 'ppsx', 'ppsm', 'sldx', 'sldm', 'thmx'],
                          'Video': ['mp4', 'm4a', 'm4v', 'f4v', 'f4a', 'm4b', 'm4r', 'f4b', 'mov', '3gp', '3gp2', '3g2', '3gpp', '3gpp2', 'ogg', 'oga', 'ogv', 'ogx', 'wmv', 'wma', 'asf', 'webm', 'flv', 'avi']}

        if file_type == 'ALL':
            self.file_type = [ext for k, v in self.extension for ext in v]

        elif file_type == 'Folders':
            self.file_type = 'Folders'

        else:
            self.file_type = self.extension[file_type]

    def already_exists(self):
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
        if os.path.isfile(file) and os.path.basename(file).split('.')[1].lower() in self.file_type:
            return True

        elif os.path.isdir(file) and self.file_type == 'Folders':
            return True

        return False

    def copy(self, file=None):
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

        return True

    def main(self):
        self.files = list(filter(self.filter_function, self.files))

        try:
            if self.already_exists():
                if not messagebox.askyesno('File Already Exists', 'Some files are already exists. Do you want to overwrite the files?'):
                    self.files = list(set(self.files) - common_files)

            for file in self.files:
                self.copy(file)

            messagebox.showinfo('Job Done', 'Job DONE')

        except FileExistsError:
            messagebox.showinfo('Directory Already Exists', 'Please! Give new directory name')

        except FileNotFoundError:
            messagebox.showinfo('Invalid Path', f'{self.to_path} is not a valid path')


class GUI:
    def __init__(self, master):
        self.__master = master
        self.__master.withdraw()
        self.__master.after(0, self.__master.deiconify)
        self.screen_width, self.screen_height = self.__master.winfo_screenwidth(), self.__master.winfo_screenheight()
        self.__master.geometry(f'400x270+{self.screen_width // 2 - 200}+{self.screen_height // 2 - 135}')
        self.__master.resizable(0, 0)
        self.font = ('Courier', 15, 'bold')
        self.__master.title('File MOVER')
        self.__master.iconbitmap('icon.ico')

        self.title_label = Label(self.__master, text='File MOVER', fg='white', background='black', font=('Times New Roman', 30, 'bold'))
        self.title_label.pack(fill='both')

        self.copy_from_entry = Entry(self.__master, fg='grey', font=self.font, width=22, highlightbackground='blue', highlightthickness=3)
        self.copy_from_entry.insert(END, 'From Path')
        self.copy_from_entry.place(x=60, y=80)

        self.copy_to_entry = Entry(self.__master, fg='grey', font=self.font, width=22, highlightbackground='blue', highlightthickness=3)
        self.copy_to_entry.insert(END, 'To Path')
        self.copy_to_entry.place(x=60, y=130)

        self.combo_box = ttk.Combobox(self.__master, value=['Folders', 'Image', 'Video', 'Audio', 'MS-Office', 'Text File', 'ALL'], width=23, height=4)
        self.combo_box.set('Select file types')
        self.combo_box.place(x=60, y=180)

        self.var = IntVar()
        self.copy_or_move_frame = Frame(self.__master)
        self.copy_radio_button = Radiobutton(self.copy_or_move_frame, text='COPY', value=1, variable=self.var, bg='dark green', activebackground='dark green', fg='black', font=self.font)
        self.move_radio_button = Radiobutton(self.copy_or_move_frame, text='MOVE', value=2, variable=self.var, bg='dark green', activebackground='dark green', fg='black', font=self.font)
        self.copy_radio_button.grid(row=0, column=0)
        self.move_radio_button.grid(row=0, column=1)
        self.copy_or_move_frame.place(x=60, y=210)

        self.do_it_button_frame = Frame(self.__master)
        self.do_it_button = Button(self.do_it_button_frame, text='DO IT !', command=self.button_command, fg='white', bg='black', activebackground='black', activeforeground='white')
        self.do_it_button.grid(row=0, column=0, ipadx=30, ipady=20)
        self.do_it_button_frame.place(x=230, y=180)

        self.copy_from_entry.bind('<Enter>', lambda e: self.enter(self.copy_from_entry, 'From Path'))
        self.copy_from_entry.bind('<Leave>', lambda e: self.leave(self.copy_from_entry, 'From Path'))

        self.copy_to_entry.bind('<Enter>', lambda e: self.enter(self.copy_to_entry, 'To Path'))
        self.copy_to_entry.bind('<Leave>', lambda e: self.leave(self.copy_to_entry, 'To Path'))

        self.__master.config(bg='green')

    def enter(self, *args):
        args[0].focus()
        args[0].config(highlightcolor='blue')

        if args[0].get() == args[1]:
            args[0].delete(0, END)
            args[0].insert(END, '')
            args[0].config(fg='black')

    def leave(self, *args):
        args[0].config(highlightcolor='blue')

        if not args[0].get():
            self.__master.focus()
            args[0].insert(END, args[-1])
            args[0].config(fg='grey')

    def button_command(self):
        from_path = self.copy_from_entry.get()
        to_path = self.copy_to_entry.get()
        combo_get = self.combo_box.get()
        var = self.var.get()

        if from_path == 'From Path' or to_path == 'To Path' or combo_get == 'Select file types' or var not in [1, 2]:
            winsound.MessageBeep()
            messagebox.showerror('Invalid Input', 'Some field(s) are left empty')

        else:
            moc = move_or_copy(from_path, to_path, combo_get, var)
            moc.main()

        os.startfile(to_path)


if __name__ == '__main__':
    root = Tk()
    GUI(root)
    root.mainloop()
