import calendar


class Yearly_Calendar:
    '''Get calendar of a given year'''

    def __init__(self, year):
        self.year = year

    def get_calendar(self):
        '''Getting calendar'''

        print('\n')
        print(calendar.calendar(self.year))


if __name__ == '__main__':
    year_calendar = Yearly_Calendar(2020)
    year_calendar.get_calendar()
