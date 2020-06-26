import calendar


def year_calendar(year):
    '''Get calendar of a given year'''

    try:
        print(calendar.calendar(year))

    except (ValueError, NameError):
        print('Integer was expected')


if __name__ == '__main__':
    year_calendar(2019)
