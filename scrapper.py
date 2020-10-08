from bs4 import BeautifulSoup
import requests
import re


class Website:

    def __init__(self, adress):
        self.website = adress

    def www(self):
        return self.website


class REPatterns:
    nwn1 = re.compile("nwn1/module")
    http = re.compile('^http://')


def request(website):
    response = requests.get(website)
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all('a', attrs={'href': REPatterns.http}):
        yield link.get('href')


def create_list_of_links():
    result = []
    for e in request(website_2.www()):
        if REPatterns.nwn1.search(e):
            result.append(e)
    return result


if __name__ == '__main__':
    website_1 = Website("http://neverwintervault.org")
    website_2 = Website("https://neverwintervault.org/article/reference/campaigns-and-module-series-list-nwn1")
