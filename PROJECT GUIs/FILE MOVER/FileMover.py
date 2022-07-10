import os
import sys
import shutil
import threading
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox


class FileMover:
    def __init__(self):
        self.value = ['ALL', 'PDF', 'Image', 'Video', 'Audio', 'Python', 'Folders', 'Programs', 'MS-Office', 'Text File', 'WinRAR']
        self.value.sort(key=len)

        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)

        self.width, self.height = 312, 260
        self.screen_width, self.screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'{self.width}x{self.height}+{self.screen_width - self.width // 2}+{self.screen_height - self.height // 2}')
        self.master.resizable(0, 0)
        self.master.title('File MOVER')
        self.master.iconbitmap(self.resource_path('icon.ico'))

        self.title_label = Label(self.master, text='File MOVER', fg='white', background='green', font=('Helvetica', 32, 'bold'))
        self.title_label.pack(pady=5)

        self.from_entry_var, self.to_entry_var = StringVar(), StringVar()
        self.from_entry_style = ttk.Style()
        self.from_entry_style.configure('F.TEntry', foreground='grey')
        self.from_entry = ttk.Entry(self.master, width=40, justify='center', textvariable=self.from_entry_var, style='F.TEntry')
        self.from_entry_var.set('From Path')
        self.from_entry.pack(ipady=2)

        self.to_entry_style = ttk.Style()
        self.to_entry_style.configure('T.TEntry', foreground='grey')
        self.to_entry = ttk.Entry(self.master, width=40, justify='center', textvariable=self.to_entry_var, style='T.TEntry')
        self.to_entry_var.set('To Path')
        self.to_entry.pack(pady=10, ipady=2)

        self.combo_box = ttk.Combobox(self.master, value=self.value, width=37, height=6)
        self.combo_box.set('Select File Types')
        self.combo_box.pack(ipady=1)

        self.style = ttk.Style()
        self.style.configure('S.TRadiobutton', foreground='white', background='green')

        self.var = IntVar()
        self.radio_submit_buttons_frame = Frame(self.master, bg='green')
        self.radio_button_frame = Frame(self.radio_submit_buttons_frame, bg='green')
        self.copy_radio_button = ttk.Radiobutton(self.radio_button_frame, text='COPY', variable=self.var, value=1, style='S.TRadiobutton', cursor='hand2')
        self.move_radio_button = ttk.Radiobutton(self.radio_button_frame, text='MOVE', variable=self.var, value=2, style='S.TRadiobutton', cursor='hand2')

        self.submit_button_frame = Frame(self.radio_submit_buttons_frame)
        self.submit_button = Button(self.submit_button_frame, text='SUBMIT', fg='white', bg='green', activebackground='green', activeforeground='white', cursor='hand2', relief=RIDGE, command=self.submit_command)

        self.copy_radio_button.grid(row=0, column=0)
        self.move_radio_button.grid(row=1, column=0)
        self.radio_button_frame.pack(side=LEFT)
        self.submit_button.grid(row=0, column=0, ipady=10, ipadx=20)
        self.submit_button_frame.pack(side=LEFT, padx=40)
        self.radio_submit_buttons_frame.pack(pady=10)

        self.master.bind('<Button-1>', self.bind_keys)
        self.to_entry.bind('<FocusIn>', self.bind_keys)
        self.to_entry.bind('<Button-1>', self.bind_keys)
        self.from_entry.bind('<FocusIn>', self.bind_keys)
        self.from_entry.bind('<Button-1>', self.bind_keys)
        self.to_entry.bind('<FocusOut>', lambda event, focus_out=True: self.bind_keys(event, focus_out))

        self.master.config(bg='green')
        self.master.mainloop()

    def bind_keys(self, event, focus_out=False):
        '''Commands when user clicks in and out of the entries widgets'''

        get_from_entry = self.from_entry_var.get().strip()
        get_to_entry = self.to_entry_var.get().strip()

        if event.widget == self.from_entry or focus_out:
            if get_from_entry == 'From Path' and not focus_out:
                self.from_entry_var.set('')
                self.from_entry_style.configure('F.TEntry', foreground='black')

            if not get_to_entry:
                self.to_entry_var.set('To Path')
                self.to_entry_style.configure('T.TEntry', foreground='grey')

        elif event.widget == self.to_entry:
            if get_to_entry == 'To Path':
                self.to_entry_var.set('')
                self.to_entry_style.configure('T.TEntry', foreground='black')

            if not get_from_entry:
                self.from_entry_var.set('From Path')
                self.from_entry_style.configure('F.TEntry', foreground='grey')

        if event.widget not in [self.from_entry, self.to_entry]:
            if not get_from_entry:
                self.from_entry_var.set('From Path')
                self.from_entry_style.configure('F.TEntry', foreground='grey')

            if not get_to_entry:
                self.to_entry_var.set('To Path')
                self.to_entry_style.configure('T.TEntry', foreground='grey')

            self.master.focus()

    def is_thread_alive(self, thread, to_path):
        '''Call this function until the thread is not finished executing. If the thread
           finished executing the restore default values to the respective widgets and
           also show th success message and open the directory where the files / folders
           are moved or copied'''

        if not thread.isAlive():    # When thread has finished executing
            self.var.set(0)

            self.from_entry_var.set('From Path')
            self.to_entry_var.set('To Path')

            self.from_entry_style.configure('F.TEntry', foreground='grey')
            self.to_entry_style.configure('T.TEntry', foreground='grey')

            self.combo_box.set('Select File Types')
            self.master.focus()

            messagebox.showinfo('Operation Successful', 'Your operation is successfully completed')
            os.startfile(to_path)

        else:    # When thread is still executing
            self.master.after(10, lambda: self.is_thread_alive(thread, to_path))

    def submit_command(self, event=None):
        '''Action when user clicks submit button'''

        from_path = self.from_entry_var.get().strip()
        to_path = self.to_entry_var.get().strip()
        file_type = self.combo_box.get()
        get_radio = self.var.get()

        if from_path in ['', 'From Path'] or to_path in ['', 'To Path'] or get_radio not in [1, 2]:
            messagebox.showerror('Invalid Entries', 'Some filed(s) are left empty')

        elif not os.path.exists(from_path) or not os.path.exists(to_path):
            messagebox.showerror('Invalid Path', 'Given From / To Path is invalid')

        else:
            mv_cp = move_or_copy(from_path, to_path, file_type, get_radio)

            thread = threading.Thread(target=mv_cp.main)
            thread.start()

            self.master.after(10, lambda: self.is_thread_alive(thread, to_path))

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


class move_or_copy:
    def __init__(self, from_path, to_path, file_type, var):
        self.var = var
        self.to_path = to_path
        self.file_type = file_type
        self.from_path = from_path
        self.extensions_list = {'PDF': 'pdf',
                                'Text File': ['txt'],
                                'Programs': ['exe', 'msi'],
                                'Audio': ['wav', 'aiff', 'mp3'],
                                'Image': ['tif', 'jpg', 'png', 'gif', 'jpeg', 'ico'],
                                'WinRAR': ['RAR', 'ZIP', '7Z', 'ARJ', 'BZ2', 'CAB', 'GZ', 'ISO', 'JAR', 'LZ', 'LZH', 'TAR', 'UUE', 'XZ', 'Z', 'ZIPX', '001'],
                                'Python': ['.py', 'py3', 'pyc', 'pyo', 'pyw', 'pyx', 'pyd', 'pxd', 'pyi', 'pyz', 'pywz', 'rpy', 'pyde', 'pyp', 'pyt', 'xpy', 'ipynb'],
                                'MS-Office': ['doc', 'docx', 'docm', 'dotx', 'dotm', 'xlsx', 'xlsm', 'xltx', 'xltm', 'xlsb', 'xlam', 'pptx', 'pptm', 'potx', 'potm', 'ppam', 'ppsx', 'ppsm', 'sldx', 'sldm', 'thmx'],
                                'Video': ['mp4', 'm4a', 'm4v', 'f4v', 'f4a', 'm4b', 'm4r', 'f4b', 'mov', '3gp', '3gp2', '3g2', '3gpp', '3gpp2', 'ogg', 'oga', 'ogv', 'ogx', 'wmv', 'wma', 'asf', 'webm', 'flv', 'avi']}

        if self.file_type == 'Folders':
            self.extensions = 'Folders'

        elif self.file_type != 'ALL':
            self.extensions = self.extensions_list[self.file_type]

    def duplicates(self, files):
        '''Checking duplicates files of from_path and to_path'''

        from_file_path = set([os.path.basename(file) for file in files])
        to_file_path = set(os.listdir(self.to_path))
        self.common_files = from_file_path & to_file_path

        if self.common_files:
            return True

        return False

    def filter_function(self, file):
        '''Filtering files as per the extension given by the user'''

        if (os.path.isfile(file) and os.path.basename(file).split('.')[1].lower() in self.extensions) or (os.path.isdir(file) and self.extensions == 'Folders'):
            return True

        return False

    def mv_or_cp(self, file):
        '''Move or Copy files and folders'''

        to_path = os.path.join(self.to_path, os.path.basename(file))

        if self.var == 1 and os.path.isfile(file):
            shutil.copy(file, to_path)

        elif self.var == 1 and os.path.isdir(file):
            shutil.copytree(file, to_path)

        elif self.var == 2:
            shutil.move(file, to_path)

    def main(self):
        '''Main function for copying/moving file/folders'''

        try:
            all_files = [os.path.join(self.from_path, f) for f in os.listdir(self.from_path)]

            if self.file_type == 'ALL':
                files = all_files

            else:
                files = list(filter(self.filter_function, all_files))

            if self.duplicates(files):
                if not messagebox.askyesno('File Already Exists', 'Some files already exists. Do you want to overwrite the files?'):
                    files = [file for file in files if file not in self.common_files]    # Removing self.common_files from files if user clicks NO

            for file in files:
                self.mv_or_cp(file)

        except FileExistsError:
            messagebox.showerror('Directory Already Exists', 'Please! Enter new directory name')


if __name__ == '__main__':
    FileMover()
