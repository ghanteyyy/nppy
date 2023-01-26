import os


class Rename_Django_Flask_Videos:
    '''
    Renames django & flask videos of Corey Schafer

    Flask Video Link: https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
    Django Video link: https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
    '''

    def __init__(self, path):
        self.path = path

    def rename_django_flask_videos(self):
        '''
        Renaming videos
        '''

        for file in os.listdir(self.path):
            split = file.split('-')

            if len(split) >= 4:
                numbers = split[2].split()[-1].zfill(2).strip()
                name = split[-1].strip()

                rename = f'{numbers} {name}'

            else:
                rename = ''.join(split[1:]).strip()

            old_path = os.path.join(self.path, file)
            new_path = os.path.join(self.path, rename)

            os.rename(old_path, new_path)


if __name__ == '__main__':
    path = '<Your Video Path>'

    django_rename = Rename_Django_Flask_Videos(path)
    django_rename.rename_django_flask_videos()

    flask_rename = Rename_Django_Flask_Videos(path)
    flask_rename.rename_django_flask_videos()
