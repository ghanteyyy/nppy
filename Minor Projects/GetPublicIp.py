import requests
from bs4 import BeautifulSoup


class GetPublicIP:
    '''
    Gets the external public IP form "myip.com"

    Still lacks flexibility. Needs to work more
    '''

    def __init__(self):
        self.servers = ['https://www.myip.com']

    def is_internet(self):
        '''
        Checks if you have internet connection
        '''

        try:
            requests.get(self.servers[0])
            return True

        except requests.ConnectionError:
            return False

    def get_html(self):
        '''
        Gets the whole html source code of the website
        '''

        return requests.get(self.servers[0]).content

    def get_ip(self):
        '''
        Getting IP
        '''

        if self.is_internet():
            html = self.get_html()

            if html:
                soup = BeautifulSoup(html, 'html.parser')
                spans = soup.find('span')

                if spans.get('id') == 'ip':
                    return spans.text

        else:
            return 'You are not connected to Internet'


if __name__ == '__main__':
    public_ip = GetPublicIP()
    print(public_ip.get_ip())
