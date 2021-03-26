import time
from tkinter import TclError
from tkinter import messagebox
import pyperclip
import find
import replace
import go_to
import search
import include


class Edit_Menu:
    def __init__(self, master, text_widget, var):
        self.var = var
        self.master = master
        self.text_widget = text_widget

    def set_var(self, text, time=4000):
        '''Config text to the status_label'''

        include.set_var(self.master, self.var, text, time)

    def get_selected_text(self):
        '''Returns text which user tends to copy or cut'''

        if 'triple_click' in self.text_widget.tag_names():
            # 'triple_click' tag is added when user triple clicks to a certain line
            # OR when user user selects all text using 'Ctrl+A' or 'Select All' menu

            return self.text_widget.get('triple_click.first', 'triple_click.last')

        else:
            try:
                # If 'triple click' tag is not found then there should be 'sel' tag
                return self.text_widget.get('sel.first', 'sel.last')

            except TclError:
                # If there is no 'triple_click' tag or 'sel' tag does not have any text
                # Then check if 'found' tag exists, if yes, then get all text from that tag

                if 'found' in self.text_widget.tag_names():
                    return self.text_widget.get('found.first', 'found.last')

        # If there is no any tags ('triple click', 'sel', 'found')
        # This indicates that user is trying to copy or cut the whole line
        # If thats the case then returning the text from beginning to end of that line
        line = self.text_widget.index('insert').split('.')[0]
        return self.text_widget.get(f'{line}.0', f'{line}.end+1c')

    def undo(self, event=None):
        '''Undo functionality when user clicks Undo option or presses Ctrl+Z'''

        try:
            self.text_widget.edit_undo()

        except TclError:
            pass

    def cut(self, event=None):
        '''Cut functionality when user clicks cut option or presses Ctrl+X'''

        text = self.get_selected_text()

        try:
            # Remove text inside 'sel' tag if available
            index = self.text_widget.index('sel.first')
            self.text_widget.delete(index, f'{index}+{len(text)}c')

        except:
            if 'found' in self.text_widget.tag_names():  # Remove text inside 'found' tag if available
                index = self.text_widget.index('found.first')
                self.text_widget.delete(index, f'{index}+{len(text)}c')

            else:  # Remove entire text from the line where the cursor is situated.
                line = self.text_widget.index('insert').split('.')[0]
                self.text_widget.delete(f'{line}.0', f'{line}.end+1c')

        pyperclip.copy(text)
        self.set_var(f'Cut {len(text)} characters')
        self.text_widget.config(insertofftime=300, insertontime=600)

        return 'break'

    def copy(self, event=None):
        '''Copy functionality when user clicks cut option or presses Ctrl+C'''

        text = self.get_selected_text()
        pyperclip.copy(text)
        self.set_var(f'Copied {len(text)} characters')

        return 'break'

    def paste(self, event=None):
        '''Paste functionality when user clicks paste option or presses Ctrl+V'''

        self.text_widget.insert(self.text_widget.index('insert'), pyperclip.paste())
        self.text_widget.see(self.text_widget.index('insert'))

        return 'break'

    def delete(self, evet=None):
        '''Remove selected character or single character after the cursor'''

        if 'triple_click' in self.text_widget.tag_names():  # Delete text that is inside 'triple click' tag
            self.text_widget.delete('triple_click.first', 'triple_click.last')
            self.text_widget.tag_delete('triple_click', '1.0', 'end')

        else:
            try:
                self.text_widget.delete("sel.first", "sel.last")  # Remove text that is inside 'sel' tag

            except TclError:
                if 'found' in self.text_widget.tag_names():  # Remove text that is inside 'found' tag
                    self.text_widget.delete('found.first', 'found.last')
                    self.text_widget.tag_delete('found')

                else:  # Remove one character infront of the cursor
                    insert_index = self.text_widget.index('insert')
                    self.text_widget.delete(insert_index, f'{insert_index}+1c')

        if self.text_widget['insertofftime'] == 1000000:  # Restore time of blinking to default
            self.text_widget.config(insertofftime=300, insertontime=600)

        self.var.set('')
        return 'break'

    def search_with_google(self, event=None):
        '''Search selected text with Google search engine'''

        text = self.get_selected_text().strip().strip('\n')

        if text:
            self.master.after(250, lambda: search.Search(self.master).open_link(f'https://www.google.com/search?q={text}'))

        else:
            messagebox.showerror('ZPAD', 'You need to select text to make search')

    def find_widget(self, event=None):
        '''Display find GUI window when user clicks find option or presses Ctrl+F'''

        find.Find(self.master, self.text_widget)

    def replace_widget(self, event=None):
        '''Display replace GUI window when user clicks find option or presses Ctrl+H'''

        replace.Replace(self.master, self.text_widget)

    def go_to_widget(self, event=None):
        '''Display Go-To GUI window when user clicks find option or presses Ctrl+G'''

        go_to.Go_To(self.master, self.text_widget)

    def select_all(self, event=None):
        '''Select all text when user clicks Select-All option or Ctrl+A'''

        from_text_widget = self.text_widget.get('1.0', 'end-1c').strip('\n')
        lines = len(from_text_widget.split('\n'))
        no_of_characters = len(from_text_widget)

        for line in range(1, lines + 1):
            self.text_widget.tag_add('sel', f'{line}.0', f'{line}.end')

        if no_of_characters > 0:
            self.set_var(text=f'{no_of_characters} characters selected', time=None)

        self.text_widget.tag_add('triple_click', '1.0', 'end-1c')
        self.text_widget.config(insertofftime=1000000, insertontime=0)

        return 'break'

    def get_date_time(self, event=None):
        '''Inserts current date and time'''

        cursor_pos = self.text_widget.index('insert')
        today_time = time.strftime('%I:%M %p %m/%d/%Y')
        cursor_index = self.text_widget.index('insert')

        try:
            if self.text_widget.get('1.0', cursor_index)[-1] != ' ':
                today_time = ' ' + today_time

        except IndexError:
            pass

        self.text_widget.insert(cursor_pos, today_time)

    def strip_whitespaces(self):
        '''Strip white-spaces from each line'''

        get_text = self.text_widget.get('1.0', 'end-1c').split('\n')
        strip_text = '\n'.join([get.rstrip().strip('\n') for get in get_text])

        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('end', strip_text)
