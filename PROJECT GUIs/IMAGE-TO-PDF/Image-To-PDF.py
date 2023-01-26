import os
import sys
import threading
from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
from PdfMaker import PdfMaker



class ImageToPDF:
    def __init__(self):
        pygame.mixer.init()

        self.AllImages = []
        self.ImageCount = 1
        self.IsErrorMsgShown = True
        self.extensions = ([('PDF', '*.pdf')])
        self.TestImagePath = 'assets/test_images'

        if sys.platform == 'win32':
            pygame.mixer.music.load(self.ResourcePath('WinErrSound.wav'))

        else:
            pygame.mixer.music.load(self.ResourcePath('LinuxErrSound.wav'))

        self.window = Tk()
        self.window.withdraw()
        self.window.title('Image-To-PDF')

        self.TextWidgetFrame = Frame(self.window, width=780, height=500)
        self.TextWidgetFrame.pack()
        self.TextWidgetFrame.propagate(0)
        self.TextWidget = Text(self.TextWidgetFrame, width=1, height=1, cursor='arrow', bg='#f2f2f2', bd=0)
        self.TextWidget.pack(side=LEFT, fill='both', expand=True)

        self.ScrollBar = ttk.Scrollbar(self.TextWidgetFrame, orient='vertical', command=self.TextWidget.yview)
        self.ScrollBar.pack(side=RIGHT, fill='y')
        self.TextWidget.config(yscrollcommand=self.ScrollBar.set)

        self.IconImage = PhotoImage(file=self.ResourcePath('icon.png'))
        self.AddButtonImage = PhotoImage(file=self.ResourcePath('Add.png'))
        self.MakePdfButtonImage = PhotoImage(file=self.ResourcePath('MakePdfButton.png'))

        self.BottomFrame = Frame(self.window)
        self.BottomFrame.pack(fill='x')
        self.MakePdfButton = Button(self.BottomFrame, image=self.MakePdfButtonImage, bd=0, cursor='hand2', command=self.MakePDF)
        self.MakePdfButton.pack(pady=10)

        self.AddButton = Button(self.window, image=self.AddButtonImage, bd=0, bg='#f2f2f2', activebackground='#f2f2f2', cursor='hand2', command=self.InsertImage)
        self.AddButton.place(in_=self.TextWidget, relx=0.91, rely=0.86)

        self.NoImageLabel = Label(self.window, text='No images to show', bg='#f2f2f2', fg='red', font=Font(size=20))
        self.NoImageLabel.place(in_=self.TextWidget, relx=0.4, rely=0.43)

        self.InsertImageInfo = Label(self.window, text='( Double click at any empty space or\npress Control + O or Click to "+"\nbutton below to insert image(s) )', fg='#f57842', font=Font(size=15))
        self.InsertImageInfo.place(in_=self.TextWidget, relx=0.34, rely=0.53)

        self.InitialPosition()

        self.window.bind('<Button-1>', self.SelectImage)
        self.window.bind('<Control-o>', self.InsertImage)
        self.window.bind('<MouseWheel>', self.MouseWheel)
        self.window.bind('<Tab>', self.RestrictDefaultBindings)
        self.TextWidget.bind('<Double-Button-1>', self.InsertImage)
        self.BottomFrame.bind('<Double-Button-1>', self.InsertImage)
        self.NoImageLabel.bind('<Double-Button-1>', self.InsertImage)
        self.InsertImageInfo.bind('<Double-Button-1>', self.InsertImage)
        self.TextWidget.bind('<Button-1>', self.RestrictDefaultBindings)

        self.window.mainloop()

    def InitialPosition(self):
        '''
        Placing window at the center of screen when the GUI starts at first
        '''

        self.window.update()
        self.window.resizable(0, 0)
        self.window.iconphoto(False, self.IconImage)

        width = self.window.winfo_width() // 2
        height = self.window.winfo_height() // 2

        screen_width = self.window.winfo_screenwidth() // 2
        screen_height = self.window.winfo_screenheight() // 2

        x = screen_width - width
        y = screen_height - height

        self.window.geometry(f'+{x}+{y}')
        self.window.deiconify()

    def RestrictDefaultBindings(self, event):
        '''
        Restrict text-widget to insert cursor when user tries by clicking into
        it or by using TAB key
        '''

        return 'break'

    def MouseWheel(self, event):
        '''
        Scrolling when user's mouse is over the image
        '''

        widget = event.widget

        if isinstance(widget, Label):
            for _ in range(2):
                widget = widget.winfo_parent()
                widget = self.window.nametowidget(widget)

        if isinstance(widget, (Text, Frame)):
            self.TextWidget.yview_scroll(int(-1*(event.delta/120)), "units")

    def InsertImage(self, event=None):
        '''
        Insert Image to the image list widget
        '''

        extensions = ([('PNG', '*.png'), ('JPG', '*jpg *jpeg')])
        images = filedialog.askopenfilenames(title='Open', defaultextension=extensions, filetypes=extensions)

        if images:
            if self.IsErrorMsgShown:
                self.IsErrorMsgShown = False
                self.NoImageLabel.place_forget()
                self.InsertImageInfo.place_forget()

            for index, image in enumerate(images):
                if image not in self.AllImages:
                    self.AllImages.append(image)
                    self.TextWidget.insert(END, ' ' * 3)  # Separating each image with three spaces

                    im = Image.open(image)
                    im = im.resize((200, 200), Image.Resampling.LANCZOS)
                    im = ImageTk.PhotoImage(im)

                    frame = Frame(self.TextWidget, width=200, height=200, bg='#f2f2f2')
                    frame.propagate(0)

                    ImageLabel = Label(frame, image=im, text=image)
                    ImageLabel.pack()
                    ImageLabel.image = im

                    self.TextWidget.window_create(END, window=frame)
                    self.window.update()
                    self.TextWidget.insert(END, '\t' * 4)

                    if (index + 1) % 3 == 0:  # Inserting new line after every three images
                        self.TextWidget.insert(END, '\n\n')

    def SelectImage(self, event):
        '''
        Insert numbers to each clicked image
        '''

        widget = event.widget

        if isinstance(widget, (Button, ttk.Scrollbar, ttk.Checkbutton, Tk)) is False and widget not in [self.NoImageLabel, self.InsertImageInfo]:
            if isinstance(widget, Label):
                widget = widget.winfo_parent()
                widget = self.window.nametowidget(widget)

            labels = [child for child in widget.winfo_children() if isinstance(child, Label)]

            if labels:
                if len(labels) == 1:  # If no number has been inserted then insert one
                    ImageNumLabel = Label(widget, text=self.ImageCount, fg='white', bg='red')
                    ImageNumLabel.place(in_=widget, x=widget.winfo_width() - ImageNumLabel.winfo_reqwidth())

                    self.ImageCount += 1

                else:
                    # When the number has been already inserted then
                    # Removing it and adjusting other numbering too
                    current_label_num = int(labels[1].cget('text'))
                    labels[-1].destroy()

                    for frame in self.TextWidget.winfo_children():  # Going through all frames
                        inner_labels = frame.winfo_children()  # Getting all widgets inside of the frame

                        # Checking if there are two labels inside frame
                        # Two labels-widget means one is image and another is image number
                        if len(inner_labels) > 1:
                            inner_labels = inner_labels[-1]
                            labels_text = inner_labels.cget('text')

                            if labels_text:
                                labels_text = int(labels_text)  # Getting number from the number-widget

                                # Checking if number of label is
                                # greater than the removed number
                                # If yes, then decreasing each number by 1
                                if labels_text > current_label_num:
                                    labels_text -= 1
                                    inner_labels.config(text=labels_text)

                    self.ImageCount -= 1

    def MakePDF(self):
        '''
        When user click Make PDF button
        '''

        images = dict()

        for frame in self.TextWidget.winfo_children():  # Going through each frame in Text-widget
            inner_labels = frame.winfo_children()  # Getting all widgets inside of the frame

            # Checking if there are two labels inside frame
            # Two labels-widget means one is image and another is image number
            if len(inner_labels) > 1:
                inner_label_image = inner_labels[0]
                inner_label_num = inner_labels[1]

                image_num = inner_label_num.cget('text')
                image_path = inner_label_image.cget('text')

                images.update({image_num: image_path})

        if images:
            keys = list(images.keys())
            keys.sort()

            images = [images[k] for k in keys]
            output_path = filedialog.asksaveasfilename(title='Save', defaultextension=self.extensions, filetypes=self.extensions)

            if output_path:
                self.maker = PdfMaker()
                thread = threading.Thread(target=self.maker.Make, args=(images, output_path,))
                thread.start()

        else:
            pygame.mixer.music.play()

    def ResourcePath(self, FileName):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or
            file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or
            file of any extension from temporary directory

        param:
            FileName: image, audio, or any other file_name present in the assets directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', FileName)


if __name__ == '__main__':
    ImageToPDF()
