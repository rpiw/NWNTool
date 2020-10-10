from bs4 import BeautifulSoup
import requests
import re
import validators
from exceptions import InvalidUrl


class Website:

    def __init__(self, address):
        if validators.url(address):
            self.website = address
        else:
            raise InvalidUrl

    def www(self):
        return self.website

    def __add__(self, other):
        return Website(self.www() + other.www())


class REPatterns:
    nwn1 = re.compile("nwn1/module")
    http = re.compile('^http://')
    module_src = re.compile("modules")

    class Module:
        strings_dict = {
                        0: "field-name-submitted-by",
                        1: "field-name-changed-date",
                        2: "field-name-field-project-version",
                        3: "field-name-field-game",
                        4: "field-name-field-category",
                        5: "field-name-field-requirements",
                        6: "field-name-field-language",
                        7: "field-name-field-tags",
                        9: "field-name-field-related-projects",
                        10: "field-name-field-permissions-licensing",
                        11: "field-name-field-required-projects"
        }


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


def scrap_nvn_vault(website: Website) -> dict:
    u"""Scrapper for page with module data on neverwintervault.org.
        Return a dictionary."""
    result = {"href": "",
              "title": "",
              "size": 0,
              "compression": "",
              "author": None,
              "last_changed": None,
              "version": "Release",
              "game": "",
              "category": "",
              "tags": [],
              "required projects": [],
              "related projects": [],
              "requirements": []
              }
    response = requests.get(website.www())
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("a", attrs={"href": REPatterns.module_src})

    # Get a link as a str
    result["href"] = website_root.www() + link["href"]

    # Get a title
    try:
        result["title"] = link["title"]
    except KeyError:
        result["title"] = "title"

    # Get a size of a file.
    result["size"] = link["type"][re.search("length=", link["type"]).end():]

    # Get a compression
    result["compression"] = link["type"][re.search("/", link["type"]).start() + 1: re.search(";", link["type"]).start()]

    # Get an author's name
    _string = soup.find("span", attrs={"class", re.compile("username")})
    if _string:
        result["author"] = re.split("/", _string["about"])[-1]

    # Get last change date
    _string = soup.find("div", attrs={"class", re.compile(REPatterns.Module.strings_dict[1])})
    if _string:
        _date = "-".join(filter(lambda x: x != '', re.split("\D", _string.text)))
        result["last_changed"] = _date

    def get_result_value(i: int, splitter=":"):
        __string = soup.find("div", attrs={"class", re.compile(REPatterns.Module.strings_dict[i])})
        if __string:
            __key, *__value = re.split(splitter, __string.text)
            __key = __key.lower()
            for item in __value:
                __value.remove(item)
                item = item.strip()
                __value.append(item)
            return __key, __value
        return None, None

    # Get a project version, game name, category in vault, language
    for i in (2, 3, 4, 6):
        key, value = get_result_value(i)
        if key and value:
            result[key] = value[0]

    # Get a tags and requirements (OC, Xp1, Xp2)
    for i in (5, 7, 9, 11):
        key, value = get_result_value(i)
        if key and value:
            result[key] = value

    return result


if __name__ == '__main__':
    website_root = Website("https://neverwintervault.org")
    website_2 = Website("https://neverwintervault.org/article/reference/campaigns-and-module-series-list-nwn1")
    website_with_module = Website("https://neverwintervault.org/project/nwn1/module/enigma-island-complete")
    website_with_patch = Website("https://neverwintervault.org/project/nwnee/other/patch/community-music-pack-fix-nwnee")
