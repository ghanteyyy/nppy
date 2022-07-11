import os
import sys
import json
import time
import requests
import threading
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font, messagebox


class WeatherForecast:
    '''
        Weather Forecast is a simple GUI program written in Python
        that gets the weather condition of given location and
        display them to the user.

            Q. How to get your API keys?
                1. Go to: https://openweathermap.org/api
                2. Sign Up with your respective emails
                3. Click API keys option
                4. Give name for your API keys [Optional]
                5. Click Generate

                Then you will get your API keys
    '''

    def __init__(self):
        self.api_key = 'Your API Key'

        self.master = Tk()
        self.master.withdraw()
        self.master.iconbitmap(self.resource_path('icon.ico'))
        self.master.title('Weather Forecast')
        self.image_obj = PhotoImage(file=self.resource_path('1.png'))
        self.image_label = Label(self.master, image=self.image_obj, bd=0)
        self.image_label.pack(pady=10)

        self.style = ttk.Style()
        self.entry_var = StringVar()
        self.entry_var.set('Location ...')
        self.style.configure('E.TEntry', foreground='grey')
        self.entry = ttk.Entry(self.master, width=35, style='E.TEntry', textvariable=self.entry_var, justify='center', font=font.Font(size=11))
        self.entry.pack(pady=10, ipady=3)

        self.button = Button(self.master, width=39, text='Show Weather', cursor='hand2', command=self.show_weather_details)
        self.button.pack(ipady=5)

        self.var = StringVar()
        self.details = Label(self.master, width=30, textvariable=self.var, justify='left', anchor='w', font=font.Font(size=11))

        self.master.config(bg='#008bff')
        self.master.after(0, self.initial_position)
        self.entry.bind('<FocusIn>', self.entry_bind)
        self.master.bind('<Button-1>', self.master_bind)
        self.entry.bind('<Return>', self.show_weather_details)
        self.entry.bind('<FocusOut>', lambda event, focus_out=True: self.entry_bind(event, focus_out))
        self.master.mainloop()

    def initial_position(self, event=None):
        '''Set position of the window to the center of the screen when user open the program'''

        self.master.update()
        self.master.resizable(0, 0)

        width, height = self.master.winfo_width() + 20, self.master.winfo_height() + 10
        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2

        self.master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')
        self.master.deiconify()

    def entry_bind(self, event=None, focus_out=False):
        '''Add or Remove default text when focused_in or focused_out from the entry_widget'''

        entry_get = self.entry_var.get().strip()

        if focus_out:
            if not entry_get:
                self.entry_var.set('Location ...')
                self.style.configure('E.TEntry', foreground='grey')

        else:
            if entry_get == 'Location ...':
                self.entry_var.set('')
                self.style.configure('E.TEntry', foreground='black')

    def master_bind(self, event=None):
        '''Set focus to maker if user outside of entry_widgets'''

        widget = event.widget

        if widget != self.entry:
            self.master.focus()

    def get_details(self, location, link):
        '''Get weather details from user given location'''

        try:
            content = requests.get(link).text
            _content = json.loads(content)

            if _content['cod'] == 401:
                messagebox.showerror('ERR', 'API key is invalid')

            elif _content['cod'] == 200:
                location = f'{"Location".ljust(31)} : {location}'
                sunrise = str(time.ctime(_content['sys']['sunrise'])).split()[-2].split(':')
                sunrise = f' : {sunrise[0].zfill(2)}:{sunrise[1].zfill(2)}:{sunrise[2].zfill(2)}'
                sunset = str(time.ctime(_content['sys']['sunset'])).split()[-2].split(':')
                sunset = f' : {sunset[0].zfill(2)}:{sunset[1].zfill(2)}:{sunset[2].zfill(2)}'

                temp = f'{"Temperature".ljust(27)} : {round(_content["main"]["temp"] - 273, 3)} °C'
                max_temp = f'{"Max Temperature".ljust(24)} : {str(round(_content["main"]["temp_max"] - 273, 3))} °C'
                min_temp = f'{"Min Temperature".ljust(25)} : {str(round(_content["main"]["temp_min"] - 273, 3))} °C'
                Humidity = f'{"Humidity".ljust(31)} : {str(_content["main"]["humidity"])} %'
                feels_like = f'{"Feels Like".ljust(31)} : {str(round(_content["main"]["feels_like"] - 273, 3))} °C'
                sky_desc = f'{"Sky".ljust(34)} : {_content["weather"][0]["description"].title()}'
                wind = f'{"Wind".ljust(33)} : {round((_content["wind"]["speed"] * 3.6), 3)} km/hr'

                details = f'''{location}\n{sky_desc}\n{Humidity}\n{temp}\n{max_temp}\n{min_temp}\n{feels_like}\n{wind}\n'''
                self.details.pack_forget()
                self.var.set(details)
                self.details.pack(pady=10)

                self.master.geometry('306x350')

            else:
                messagebox.showerror('ERR', 'Location Not Found')

        except requests.ConnectionError:
            messagebox.showerror('ERR', 'No Internet Connection')

    def show_weather_details(self, event=None):
        '''Get weather details and display them to the user'''

        location = self.entry_var.get().strip().title()
        link = f"https://api.openweathermap.org/data/2.5/weather?q={location.replace(' ', '%20')}&appid={self.api_key}"

        thread = threading.Thread(target=self.get_details, args=[location, link])
        thread.start()

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


if __name__ == '__main__':
    WeatherForecast()
