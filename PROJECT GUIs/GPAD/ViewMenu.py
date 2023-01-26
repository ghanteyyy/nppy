import Include
from tkinter import BooleanVar


class Zoom:
    def __init__(self, zoom_label, font):
        self.font = font
        self.Zoomed = 0
        self.ZoomCount = 100
        self.ZoomLabel = zoom_label

    def ZoomIn(self, event=None):
        '''
        Increase font_size upto 50 times from default_size
        '''

        if self.ZoomCount != 500:  # 500% is the maximum percentage to zoom-in
            self.Zoomed += 1
            font_size = self.font['size'] + 1
            self.font.configure(size=font_size)

            self.ZoomCount += 10
            self.ZoomLabel['text'] = f'{self.ZoomCount}%'
            self.SaveZoom(self.Zoomed)

    def ZoomOut(self, event=None):
        '''
        Decrease font_size upto 10 times from default_size
        '''

        if self.ZoomCount != 10:  # 10% is the minimum percentage to zoom-out
            self.Zoomed -= 1
            font_size = self.font['size'] - 1

            if font_size != 0:
                self.font.configure(size=font_size)

            self.ZoomCount -= 10
            self.ZoomLabel['text'] = f'{self.ZoomCount}%'
            self.SaveZoom(self.Zoomed)

    def DefaultZoom(self, event=None):
        '''
        Change zoomed_in and zoomed_out fonts to the default_size
        '''

        self.ZoomCount = 100
        self.ZoomLabel['text'] = '100%'
        self.SaveZoom()

    def SaveZoom(self, zoomed=None):
        '''
        Save the amount of zoom in and zoom out to the json file
        '''

        font_details = Include.GetFontDetails()

        if zoomed is None:  # This means remove zoomed amount
            self.Zoomed = 0

            if 'Zoomed' in font_details:
                font_details.pop('Zoomed')

            self.font.configure(family=font_details['Font Family'], size=font_details['Font Size'])

        else:
            font_details['Zoomed'] = self.Zoomed

        Include.SaveFontDetails(font_details)


class LineNumber:
    '''
    Update line numbers
    '''

    def __init__(self, master, line_canvas, text_widget, font):
        self.font = font
        self.master = master
        self.LineCanvas = line_canvas
        self.TextWidget = text_widget

    def redraw(self):
        '''
        Draw line number when the cursor goes to new line
        '''

        self.LineCanvas.delete("all")
        i = self.TextWidget.index("@0,0")

        while True:
            d_line = self.TextWidget.dlineinfo(i)

            if d_line is None:
                break

            y = d_line[1]
            line_num = str(i).split(".")[0]

            font = (self.font['family'], self.font['size'])
            self.LineCanvas.create_text(2, y, anchor="nw", text=line_num, font=font)
            i = self.TextWidget.index("%s+1line" % i)

        self.master.after(100, self.redraw)


class View:
    def __init__(self, master, text_widget, text_widget_frame, canvas_frame, line_canvas, status_bar_frame, zoom_label, font):
        self.master = master
        self.LineCanvas = line_canvas
        self.TextWidget = text_widget
        self.CanvasFrame = canvas_frame
        self.Zoom = Zoom(zoom_label, font)
        self.StatusBarFrame = status_bar_frame
        self.TextWidgetFrame = text_widget_frame
        self.LineNumber = LineNumber(master, line_canvas, text_widget, font)

        self.ShowStatusBar = BooleanVar(value=True)
        self.FullScreenVar = BooleanVar(value=False)
        self.LineNumberVar = BooleanVar(value=False)

    def ZoomIn(self, event=None):
        self.Zoom.ZoomIn()

    def ZoomOut(self, event=None):
        self.Zoom.ZoomOut()

    def DefaultZoom(self, event=None):
        self.Zoom.DefaultZoom()

    def WheelZoom(self, event=None):
        '''
        Zoom in or out when pinching in and out on mousepad
        '''

        if event.state == 44:
            if event.delta > 0:
                self.Zoom.ZoomIn()

            else:
                self.Zoom.ZoomOut()

            return 'break'

    def toggle_statusbar(self, event=None):
        '''
        Show or hide status-bar when user clicks Status-bar sub-menu in View
        menu or when user presses Alt+S
        '''

        if self.ShowStatusBar:
            self.ShowStatusBar = False
            self.StatusBarFrame.grid_forget()

        else:
            self.ShowStatusBar = True
            self.StatusBarFrame.grid(row=2, column=0, sticky='e')

    def set_full_screen(self, event=None):
        '''
        Change window to full-screen when user user clicks FullScreen sub-menu
        in View-Menu or when presses F11
        '''

        state = False if self.master.wm_attributes('-fullscreen') else True
        self.master.wm_attributes('-fullscreen', state)

    def ToggleLineNumber(self, event=None):
        '''
        Hide and show line_number
        '''

        if self.LineNumberVar:
            self.LineNumberVar = False
            self.CanvasFrame.pack_forget()

        else:
            self.LineNumberVar = True
            self.CanvasFrame.pack(side='left', fill='y')
            self.TextWidgetFrame.pack(side='right', fill='both', expand=True)
            self.LineNumber.redraw()
            self.LineCanvas.configure(scrollregion=self.LineCanvas.bbox('all'))
