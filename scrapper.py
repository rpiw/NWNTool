from bs4 import BeautifulSoup
import requests
import re


class Website:

    def __init__(self, address):
        self.website = address

    def www(self):
        return self.website


class REPatterns:
    nwn1 = re.compile("nwn1/module")
    http = re.compile('^http://')
    module_src = re.compile("modules")

    class Module:
        strings_list = [
                        "field-name-submitted-by",
                        "field-name-changed-date",
                        "field-name-field-project-version",
                        "field-name-field-game",
                        "field-name-field-category",
                        "field-name-field-requirements",
                        "field-name-field-language",
                        "field-name-field-tags",
                        "field-name-field-files",
                        "field-name-field-related-projects",
                        "field-name-field-permissions-licensing"
                        ]
        module = tuple(re.compile(x) for x in strings_list)


def request(website: Website):
    response = requests.get(website.www())
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all('a', attrs={'href': REPatterns.http}):
        yield link.get('href')


def create_list_of_links() -> list:
    result = []
    for e in request(website_2.www()):
        if REPatterns.nwn1.search(e):
            result.append(e)
    return result


def scrap_nwn_module(website: Website) -> dict:
    u"""Scrapper for page with module data on neverwintervault.org.
        Return a dictionary."""
    result = {"href": "",
              "title": "",
              "size": 0,
              "compression": "",
              "author": None,
              "last_changed": None,
              "project_version": 0,
              "game": "",
              "category": "",
              "tags": [],
              "related-projects": [],
              "license": ""
              }
    response = requests.get(website.www())
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("a", attrs={"href": REPatterns.module_src})

    # Get a link as a str
    result["href"] = website_root.www() + link["href"]
    # Get a title
    result["title"] = link["title"]
    # Get a size of a file.
    result["size"] = link["type"][re.search("length=", link["type"]).end():]
    # Get a compression
    result["compression"] = link["type"][re.search("/", link["type"]).start() + 1: re.search(";", link["type"]).start()]

    return result


if __name__ == '__main__':
    website_root = Website("https://neverwintervault.org")
    website_2 = Website("https://neverwintervault.org/article/reference/campaigns-and-module-series-list-nwn1")
    website_with_module = Website("https://neverwintervault.org/project/nwn1/module/enigma-island-complete")
    scrap_nwn_module(website_with_module)
