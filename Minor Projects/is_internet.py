import requests


def is_internet():
    '''Check if you are connected to internet'''

    try:
        requests.get("http://www.google.com")
        return True

    except requests.ConnectionError:
        return False


if is_internet():
    print('Internet Access')

else:
    print('No Internet')
