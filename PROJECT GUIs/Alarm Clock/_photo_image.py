import Include
from tkinter import PhotoImage


class Image:
    def __init__(self):
        self.on_image = PhotoImage(file=Include.ResourcePath('on.png'))
        self.off_image = PhotoImage(file=Include.ResourcePath('off.png'))
        self.add_image = PhotoImage(file=Include.ResourcePath('add.png'))
        self.del_image = PhotoImage(file=Include.ResourcePath('del.png'))
        self.icon_image = PhotoImage(file=Include.ResourcePath('icon.png'))
        self.tick_image = PhotoImage(file=Include.ResourcePath('tick.png'))
        self.cancel_alarm_image = PhotoImage(file=Include.ResourcePath('cancel.png'))

        self.WinErrAudio = Include.ResourcePath('WinErrSound.wav')
        self.LinuxErrAudio = Include.ResourcePath('LinuxErrSound.wav')
