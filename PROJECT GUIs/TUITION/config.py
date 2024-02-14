import os
import json


class Config:
    def __init__(self):
        self.contents = dict()
        self.ROOT_PATH = os.path.join(os.environ['USERPROFILE'], r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Tuition')

        if os.path.exists(self.ROOT_PATH) is False:
            os.mkdir(self.ROOT_PATH)

        self.SettingsFile = os.path.join(self.ROOT_PATH, 'settings.json')
        self.GetContents()

    def SetDefaultValues(self):
        '''
        Default values required for setting file
        '''

        defaultValues = {
            'Is-Running': False,
            'Is-Minimized': False,
            'From-StartUp': False
        }

        db_dir = self.contents.get('db_dir', None)

        if db_dir:
            defaultValues.update({'db_dir': db_dir})

        is_added_to_startup = self.contents.get('Is-Added-To-Startup', False)
        defaultValues.update({'Is-Added-To-Startup': is_added_to_startup})

        return self.WriteContents(defaultValues)

    def GetContents(self):
        '''
        Get the contents of setting file
        '''

        try:
            with open(self.SettingsFile, 'r') as f:
                self.contents = json.load(f)

        except (json.JSONDecodeError, FileNotFoundError):
            self.contents = self.SetDefaultValues()

        return self.contents

    def WriteContents(self, contents):
        ''''
        Write the updated value(s) in setting file
        '''

        with open(self.SettingsFile, 'w') as f:
            json.dump(contents, f, indent=4)

        return contents

    def ToggleValues(self, key, value):
        '''
        Set value as per provided key
        '''

        self.contents = self.GetContents()
        self.contents[key] = value

        self.WriteContents(self.contents)

