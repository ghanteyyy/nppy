import calendar


class MonthlyCalendar:
    '''
    Prints calendar of a given year and month
    '''

    def __init__(self, year=2020, month='Jun'):
        self.year = year
        self.month = month
        self.all_months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
                           'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 10}

    def get_calendar(self):
        '''
        Getting Calendar
        '''

        if self.month in self.all_months:
            month_num = self.all_months[self.month]
            Calendar = calendar.month(self.year, month_num)

            return Calendar

        else:
            return 'Invalid Month'


if __name__ == '__main__':
    month_calendar = MonthlyCalendar()
    print(month_calendar.get_calendar())
