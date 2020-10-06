from bs4 import BeautifulSoup
import requests

website_1 = "http://neverwintervault.org"
website_2 = "https://neverwintervault.org/article/reference/campaigns-and-module-series-list-nwn1"


class Scrapper:
    u"""Scrapper for http://neverwintervault.org"""

    def request(self, website):
        response = requests.get(website)
        print(response.text)


if __name__ == '__main__':
    Scrapper().request(website_2)
