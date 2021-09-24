import include
from tkinter import BooleanVar


class Zoom:
    def __init__(self, zoom_label, font):
        self.font = font
        self.zoomed = 0
        self.zoom_count = 100
        self.zoom_label = zoom_label

    def zoom_in(self, event=None):
        '''Increase font_size by 1 upto 50 times from default_size'''

        if self.zoom_count != 500:  # 500% is the maximum perecentage to zoom-in
            self.zoomed += 1
            font_size = self.font['size'] + 1
            self.font.configure(size=font_size)

            self.zoom_count += 10
            self.zoom_label['text'] = f'{self.zoom_count}%'
            self.save_zoomed(self.zoomed)

    def zoom_out(self, event=None):
        '''Decrease font_size by 1 upto 10 times from default_size'''

        if self.zoom_count != 10:  # 10% is the minimum percentage to zoom-out
            self.zoomed -= 1
            font_size = self.font['size'] - 1

            if font_size != 0:
                self.font.configure(size=font_size)

            self.zoom_count -= 10
            self.zoom_label['text'] = f'{self.zoom_count}%'
            self.save_zoomed(self.zoomed)

    def default_zoom(self, event=None):
        '''Change zoomed_in and zoomed_out fonts to the default_size'''

        self.zoom_count = 100
        self.zoom_label['text'] = '100%'
        self.save_zoomed()

    def save_zoomed(self, zoomed=None):
        '''Save the amount of zoom in and zoom out to the json file'''

        font_details = include.get_font_details()

        if zoomed is None:  # This means remove zoomed amount
            self.zoomed = 0

            if 'Zoomed' in font_details:
                font_details.pop('Zoomed')

            self.font.configure(family=font_details['Font Family'], size=font_details['Font Size'])

        else:
            font_details['Zoomed'] = self.zoomed

        include.save_font_details(font_details)


class LineNumber:
    '''Update line numbers'''

    def __init__(self, master, line_canvas, text_widget, font):
        self.font = font
        self.master = master
        self.line_canvas = line_canvas
        self.text_widget = text_widget

    def redraw(self):
        '''Draw line number when the cursor goes to new line'''

        self.line_canvas.delete("all")
        i = self.text_widget.index("@0,0")

        while True:
            dline = self.text_widget.dlineinfo(i)

            if dline is None:
                break

            y = dline[1]
            linenum = str(i).split(".")[0]

            font = (self.font['family'], self.font['size'])
            self.line_canvas.create_text(2, y, anchor="nw", text=linenum, font=font)
            i = self.text_widget.index("%s+1line" % i)

        self.master.after(100, self.redraw)


class View:
    def __init__(self, master, text_widget, text_widget_frame, canvas_frame, line_canvas, status_bar_frame, zoom_label, font):
        self.master = master
        self.line_canvas = line_canvas
        self.text_widget = text_widget
        self.canvas_frame = canvas_frame
        self.zoom = Zoom(zoom_label, font)
        self.status_bar_frame = status_bar_frame
        self.text_widget_frame = text_widget_frame
        self.line_number = LineNumber(master, line_canvas, text_widget, font)

        self.show_status_bar = BooleanVar(value=True)
        self.fullscreen_var = BooleanVar(value=False)
        self.line_number_var = BooleanVar(value=False)

    def zoom_in(self, evet=None):
        self.zoom.zoom_in()

    def zoom_out(self, evet=None):
        self.zoom.zoom_out()

    def default_zoom(self, evet=None):
        self.zoom.default_zoom()

    def wheel_zoom(self, event=None):
        '''Zoom in or out when pinching in and out on mousepad'''

        if event.state == 44:
            if event.delta > 0:
                self.zoom.zoom_in()

            else:
                self.zoom.zoom_out()

            return 'break'

    def toggle_statusbar(self, event=None):
        '''Show or hide status-bar when user clicks Status-bar sub-menu in
           View menu or when user presses Alt+S'''

        if self.show_status_bar:
            self.show_status_bar = False
            self.status_bar_frame.grid_forget()

        else:
            self.show_status_bar = True
            self.status_bar_frame.grid(row=2, column=0, sticky='e')

    def set_full_screen(self, event=None):
        '''Change window to full-screen when user user clicks FullScreen
           sub-menu in View-Menu or when presses F11'''

        state = False if self.master.wm_attributes('-fullscreen') else True
        self.master.wm_attributes('-fullscreen', state)

    def toggle_linenumber(self, event=None):
        '''Hide and show line_number'''

        if self.line_number_var:
            self.line_number_var = False
            self.canvas_frame.pack_forget()

        else:
            self.line_number_var = True
            self.canvas_frame.pack(side='left', fill='y')
            self.text_widget_frame.pack(side='right', fill='both', expand=True)
            self.line_number.redraw()
            self.line_canvas.configure(scrollregion=self.line_canvas.bbox('all'))
