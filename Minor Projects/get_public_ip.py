try:
    import ipgetter

except (NameError, ImportError, ModuleNotFoundError):
    print('ipgetter installed not found')


def get_public_ip():
    # Get your public ip address

    myip = ipgetter.myip()    # Getting your ip
    print(myip)


if __name__ == '__main__':
    get_public_ip()
