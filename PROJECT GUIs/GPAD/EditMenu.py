import time
from tkinter import TclError
from tkinter import messagebox
import pyperclip
import Find
import Replace
import GoTo
import Search
import Include


class Edit_Menu:
    def __init__(self, master, text_widget, var):
        self.var = var
        self.master = master
        self.TextWidget = text_widget

    def SetVar(self, text, time=4000):
        '''
        Config text to the status_label
        '''

        Include.set_var(self.master, self.var, text, time)

    def GetSelectedText(self):
        '''
        Returns text which user tends to copy or cut
        '''

        if 'TripleClick' in self.TextWidget.tag_names():
            # 'TripleClick' tag is added when user triple clicks to a certain line
            # OR when user user selects all text using 'Ctrl+A' or 'Select All' menu

            return self.TextWidget.get('TripleClick.first', 'TripleClick.last')

        else:
            try:
                # If 'triple click' tag is not found then there should be 'sel' tag
                return self.TextWidget.get('sel.first', 'sel.last')

            except TclError:
                # If there is no 'TripleClick' tag or 'sel' tag does not have any text
                # Then check if 'found' tag exists, if yes, then get all text from that tag

                if 'found' in self.TextWidget.tag_names():
                    return self.TextWidget.get('found.first', 'found.last')

        # If there is no any tags ('triple click', 'sel', 'found')
        # This indicates that user is trying to copy or cut the whole line
        # If thats the case then returning the text from beginning to end of that line
        line = self.TextWidget.index('insert').split('.')[0]
        return self.TextWidget.get(f'{line}.0', f'{line}.end+1c')

    def undo(self, event=None):
        '''
        Undo functionality when user clicks Undo option or presses Ctrl+Z
        '''

        try:
            self.TextWidget.edit_undo()

        except TclError:
            pass

    def cut(self, event=None):
        '''
        Cut functionality when user clicks cut option or presses Ctrl+X
        '''

        text = self.GetSelectedText()

        try:
            # Remove text inside 'sel' tag if available
            index = self.TextWidget.index('sel.first')
            self.TextWidget.delete(index, f'{index}+{len(text)}c')

        except:
            if 'found' in self.TextWidget.tag_names():  # Remove text inside 'found' tag if available
                index = self.TextWidget.index('found.first')
                self.TextWidget.delete(index, f'{index}+{len(text)}c')

            else:  # Remove entire text from the line where the cursor is situated.
                line = self.TextWidget.index('insert').split('.')[0]
                self.TextWidget.delete(f'{line}.0', f'{line}.end+1c')

        pyperclip.copy(text)
        self.SetVar(f'Cut {len(text)} characters')
        self.TextWidget.config(insertofftime=300, insertontime=600)

        return 'break'

    def copy(self, event=None):
        '''
        Copy functionality when user clicks cut option or presses Ctrl+C
        '''

        text = self.GetSelectedText()
        pyperclip.copy(text)
        self.SetVar(f'Copied {len(text)} characters')

        return 'break'

    def paste(self, event=None):
        '''
        Paste functionality when user clicks paste option or presses Ctrl+V
        '''

        try:
            self.TextWidget.delete('sel.first', 'sel.last')
            self.TextWidget.delete('TripleClick.first', 'TripleClick.last')

        except TclError:
            pass

        self.TextWidget.insert(self.TextWidget.index('insert'), pyperclip.paste())
        self.TextWidget.see(self.TextWidget.index('insert'))
        self.TextWidget.config(insertofftime=300, insertontime=600)

        return 'break'

    def delete(self, event=None):
        '''
        Remove selected character or single character after the cursor
        '''

        if 'TripleClick' in self.TextWidget.tag_names():  # Delete text that is inside 'triple click' tag
            self.TextWidget.delete('TripleClick.first', 'TripleClick.last')
            self.TextWidget.tag_delete('TripleClick', '1.0', 'end')

        else:
            try:
                self.TextWidget.delete("sel.first", "sel.last")  # Remove text that is inside 'sel' tag

            except TclError:
                if 'found' in self.TextWidget.tag_names():  # Remove text that is inside 'found' tag
                    self.TextWidget.delete('found.first', 'found.last')
                    self.TextWidget.tag_delete('found')

                else:  # Remove one character in-front of the cursor
                    insert_index = self.TextWidget.index('insert')
                    self.TextWidget.delete(insert_index, f'{insert_index}+1c')

        if self.TextWidget['insertofftime'] == 1000000:  # Restore time of blinking to default
            self.TextWidget.config(insertofftime=300, insertontime=600)

        self.var.set('')
        return 'break'

    def SearchWithGoogle(self, event=None):
        '''
        Search selected text with Google search engine
        '''

        text = self.GetSelectedText().strip().strip('\n')

        if text:
            self.master.after(250, lambda: Search.Search(self.master).OpenLink(f'https://www.google.com/search?q={text}'))

        else:
            messagebox.showerror('GPAD', 'You need to select text to make search')

    def FindWidget(self, event=None):
        '''
        Display find GUI when user clicks find option or presses Ctrl+F
        '''

        Find.Find(self.master, self.TextWidget)

    def ReplaceWidget(self, event=None):
        '''
        Display replace GUI when user clicks find option or presses Ctrl+H
        '''

        Replace.Replace(self.master, self.TextWidget)

    def GoToWidget(self, event=None):
        '''
        Display Go-To GUI when user clicks find option or presses Ctrl+G
        '''

        GoTo.Go_To(self.master, self.TextWidget)

    def SelectAll(self, event=None):
        '''
        Select all text when user click Select-All option or Ctrl+A
        '''

        from_text_widget = self.TextWidget.get('1.0', 'end-1c').strip('\n')
        lines = len(from_text_widget.split('\n'))
        no_of_characters = len(from_text_widget)

        for line in range(1, lines + 1):
            self.TextWidget.tag_add('sel', f'{line}.0', f'{line}.end')

        self.TextWidget.tag_delete('sel')

        if no_of_characters > 0:
            self.SetVar(text=f'{no_of_characters} characters selected', time=None)

        self.TextWidget.tag_add('TripleClick', '1.0', 'end-1c')
        self.TextWidget.config(insertofftime=1000000, insertontime=0)

        return 'break'

    def GetDateTime(self, event=None):
        '''
        Inserts current date and time
        '''

        cursor_pos = self.TextWidget.index('insert')
        today_time = time.strftime('%I:%M %p %m/%d/%Y')
        cursor_index = self.TextWidget.index('insert')

        try:
            if self.TextWidget.get('1.0', cursor_index)[-1] != ' ':
                today_time = ' ' + today_time

        except IndexError:
            pass

        self.TextWidget.insert(cursor_pos, today_time)

    def StripWhitespaces(self):
        '''
        Strip white-spaces from each line
        '''

        get_text = self.TextWidget.get('1.0', 'end-1c').split('\n')
        strip_text = '\n'.join([get.rstrip().strip('\n') for get in get_text])

        self.TextWidget.delete('1.0', 'end')
        self.TextWidget.insert('end', strip_text)
