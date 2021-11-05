import webbrowser
from tkinter import messagebox
import requests


class Search:
    def __init__(self, master):
        self.master = master

    def is_internet(self, link):
        '''Check if user is connected to internet'''

        try:
            requests.get(link)
            return True

        except requests.ConnectionError:
            return False

    def OpenLink(self, link):
        '''Open link to the user's default browser'''

        if self.is_internet(link):
            webbrowser.open(link)

        else:
            messagebox.showinfo('No Internet', f'Could not open "{link}"', parent=self.master)
