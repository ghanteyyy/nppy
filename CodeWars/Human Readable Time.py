def make_readable(seconds):
    split = str(seconds / 3600).split('.')
    hour = split[0].zfill(2)

    calc = str(float('0.' + split[1]) * 60).split('.')
    minute = calc[0].zfill(2)

    calc = float('0.' + calc[1]) * 60
    sec = str(int(round(calc, 0))).zfill(2)

    if sec == '60':
        sec = '00'

    return f'{hour}:{minute}:{sec}'


print(make_readable(0))   # , "00:00:00")
print(make_readable(5))   # , "00:00:05")
print(make_readable(60))   # , "00:01:00")
print(make_readable(86399))   # , "23:59:59")
print(make_readable(359999))   # , "99:59:59")
