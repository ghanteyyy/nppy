import FontUI
from tkinter import BooleanVar


class Format:
    def __init__(self, master, text_widget, font):
        self.font = font
        self.master = master
        self.TextWidget = text_widget
        self.WrapAroundVar = BooleanVar(value=False)

    def FontSelection(self, event=None):
        '''Display GUI window for font selection'''

        FontUI.UI(self.master, self.font)

    def WrapAround(self, event=None):
        '''Insert word to the new-line if it does not fit to the same line when
           enabled. Option is available in Format-Menu or Ctrl+W'''

        if self.WrapAroundVar:
            self.WrapAroundVar = False
            self.TextWidget.config(wrap='none')

        else:
            self.WrapAroundVar = True
            self.TextWidget.config(wrap='word')
