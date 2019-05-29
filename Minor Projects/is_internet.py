try:
    import requests         # This module allows to send all kinds of HTTP requests

except (ImportError, ModuleNotFoundError):
    print('requests package installed not found')


def is_internet():
    '''Check your internet conection'''

    try:
        requests.get("http://www.google.com")
        return True

    except requests.ConnectionError:
        return False


if is_internet():
    print('Internet Access')

else:
    print('No Internet')
