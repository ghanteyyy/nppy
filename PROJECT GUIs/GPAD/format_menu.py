import font_ui
from tkinter import BooleanVar


class Format:
    def __init__(self, master, text_widget, font):
        self.font = font
        self.master = master
        self.text_widget = text_widget
        self.wrap_around_var = BooleanVar(value=False)

    def font_selection(self, event=None):
        '''Display GUI window for font selection'''

        font_ui.UI(self.master, self.font)

    def wrap_around(self, event=None):
        '''Insert word to the new-line if it does not fit to the same line when
           enabled. Option is available in Format-Menu or Ctrl+W'''

        if self.wrap_around_var:
            self.wrap_around_var = False
            self.text_widget.config(wrap='none')

        else:
            self.wrap_around_var = True
            self.text_widget.config(wrap='word')
