import calendar


def month_calendar(year, month):
    '''Prints calendar of a given month and year'''

    try:
        month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
                      'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        if month in month_list:
            month_num = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11,
                         'December': 10, 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

            print(calendar.month(year, month_num[month]))

        else:
            print(calendar.month(year, month))

    except (ValueError, NameError):
        print('Both [Year] and [month] argument as integer')


if __name__ == '__main__':
    month_calendar(2019, 'Apr')
