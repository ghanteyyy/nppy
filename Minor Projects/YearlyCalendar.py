import calendar


class YearlyCalendar:
    '''
    Get calendar of a given year
    '''

    def __init__(self, year):
        self.year = year

    def get_calendar(self):
        '''
        Getting calendar
        '''

        print('\n')
        print(calendar.calendar(self.year))


if __name__ == '__main__':
    year_calendar = YearlyCalendar(2020)
    year_calendar.get_calendar()
