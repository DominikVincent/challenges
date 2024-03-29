import hashlib
import urllib.parse
from datetime import datetime
import io
import json
import re
from typing import Iterator, Match
from html import escape

import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image
from bs4 import BeautifulSoup
from pywebio.input import actions, input
from pywebio.output import put_markdown, put_image, use_scope, put_text
from pywebio.session import set_env
from more_itertools import peekable

# API_URL = "https://test.wikipedia.org/w/api.php"
API_URL = "https://en.wikipedia.org/w/api.php"

BOT_NAME = "Sockenmonster@alttool"
BOT_PASSWORD = "edetgvj8m2j27hlqih1fre9qbmih39f0"

def query_webpage(webpage: str) -> str:
    """
    Queries webpage and returns it

    @:param - url from webpage
    """
    # Query a random Wikipedia page
    page = requests.get(webpage)

    print(page.url)

    # Parse the HTML
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup, page.url


def random_webpage():
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/Special:Random')
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/Ritual')
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/User:Sockenmonster/sandbox')
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/Djamin_Ginting')
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/New_York_State_Route_118')
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/Ty_Tabor')
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/2020_WNBL_season')
    # TODO add support for galleries as below
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/Scottish_National_Portrait_Gallery')
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/Criollas_de_Caguas')
    # soup, url = query_webpage('https://en.wikipedia.org/wiki/Jean_Paul')

    # title = url.split("/")[-1]
    title = "User:Sockenmonster/sandbox"
    # TODO use nicer alternative: https://en.wikipedia.org/w/index.php?title=Google&action=raw

    # TODO add image info in that api call. Images only returns titles but not urls, imageinfo does not return anything
    wikitext_params = {
        "action": "query",
        "prop": "revisions",
        # "titles": title,
        "generator": "random",
        "grnnamespace": 0,
        "rvslots": "*",
        "rvprop": "ids|timestamp|content",
        "formatversion": 2,
        "curtimestamp": True,
        "format": "json"
    }
    wikitext = requests.get(API_URL, params=wikitext_params)

    # TODO investigate why the images json response is sometimes empty, e.g. 2020_WNBL_season
    try:
        query = json.loads(wikitext.content.decode("utf-8"))["query"]
        print(query)
        source = query["pages"][0]["revisions"][0]["slots"]["main"]["content"]


        title = query["pages"][0]["title"]
        image_params = {
            "action": "query",
            "titles": title,
            "generator": "images",
            "gimlimit": 50,
            "prop": "imageinfo",
            "iiprop": "url|dimensions|mime",
            "format": "json"
        }
        images_raw = requests.get(API_URL, image_params)
        images = json.loads(images_raw.content.decode("utf-8"))["query"]["pages"]

        meta = {
            "title": title,
            "revid": query["pages"][0]["revisions"][0]["revid"],
            "timestamp": query["pages"][0]["revisions"][0]["timestamp"],
        }

    except KeyError:
        print("experienced Keyerror")
        return title, None, None, None

    return title, source, images, meta


def get_title(soup):
    title = soup.find('title').contents[0]

    return title


def get_all_matches(wikitext: str, filename: str) -> Iterator[Match[str]]:
    """
    returns all match objects for a given filename. The group covers everything after |
    :param wikitext:
    :param filename:
    :return:
    """
    filename = re.escape(filename)

    return re.finditer(r"\[\[" + filename + r"\s*\|(?P<match>(.*?(?:\[\[.*?\]\])*.*?)*)\]\]", wikitext,
                       flags=re.IGNORECASE)


def update_wikitext_alt(wikitext: str, match: re.Match, alt_text: str, offset: int) -> str:
    if "alt" in match.group("match"):
        # Handle replacement
        alt_pos_match = re.search(r"\|\s*alt\=(.*?)(?:\]|\||$)", match.group("match"), flags=re.IGNORECASE)

        wikitext = wikitext[:match.start(1) + alt_pos_match.start(1) + offset] + alt_text + \
                   wikitext[match.start(1) + alt_pos_match.end(1) + offset:]
    else:
        # Add the alt text
        wikitext = wikitext[:match.end(1) + offset] + f"|alt={alt_text}" + wikitext[match.end(1) + offset:]
    return wikitext


def get_alt_text(match):
    """
    Returns the alt text of an [[File:filename|...]] wikitext embedding
    :param match:
    :return:
    """
    if "alt" in match.group("match"):
        # Handle replacement
        alt_pos_match = re.search(r"\|\s*alt=(.*?)(?:\]|\||$)", match.group("match"), flags=re.IGNORECASE)
        return alt_pos_match.group(1)
    return ""


def get_csrf_token(session, login_token) -> str:
    login_params = {
        "action": "login",
        "lgname": BOT_NAME,
        "lgpassword": BOT_PASSWORD,
        "lgtoken": login_token,
        "format": "json"
    }

    # Login here
    resp = session.post(url=API_URL, data=login_params)
    data = resp.json()
    if data["login"]["result"] != "Success":
        return ""

    csrf_params = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    resp = session.get(url=API_URL, params=csrf_params)
    data = resp.json()

    csrf_token = data['query']['tokens']['csrftoken']

    return csrf_token


def get_login_token(session):
    """
    taken from https://www.mediawiki.org/wiki/API:Edit
    :param session:
    :return:
    """

    # Step 1: GET request to fetch login token
    login_params = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    r = session.get(url=API_URL, params=login_params)
    data = r.json()
    login_token = data['query']['tokens']['logintoken']
    return login_token

def send_edit_update(wikitext: str, meta: dict):
    session = requests.Session()

    login_token = get_login_token(session)

    csrf_token = get_csrf_token(session, login_token)
    if csrf_token == "":
        return False

    today = datetime.now()
    iso_date = today.isoformat()

    wikitext_utf_8 = escape(wikitext)
    edit_params = {
        "action": "edit",
        "title": meta["title"],
        "text": wikitext_utf_8,
        "summary": "add alt field info. Done via alt tool.",
        "minor": True,
        "bot": True,
        "baserevid": meta["revid"],
        "basetimestamp": meta["timestamp"],
        "starttimestamp": iso_date,
        "nocreate": True,
        # TODO use hashsum
        # "md5": hashlib.md5(wikitext_utf_8).hexdigest(),
        # TODO figure out what this has to be set to if used.
        # "contentformat": "text/plain",
        # "contentmodel": "wikitext",
        "token": csrf_token,
        "format": "json",
    }
    # TODO use multipart/formdata
    resp = session.post(API_URL, data=edit_params)
    print(resp.text)

    if not resp.ok:
        return False
    resp_json = resp.json()
    return "error" not in resp_json

def user_updates():
    set_env(title="Alt Text Tool")

    finished = False
    while not finished:

        title, wikitext, images, meta = random_webpage()
        if wikitext is None or images is None:
            continue
        # Ensure that random wikipage has images
        while len(images) == 0:
            title, wikitext, images = random_webpage()

        print("title: ", title)
        with use_scope('wikipage', clear=True):
            put_markdown(f'# Alt Text Update Tool: {title}')

            images_edits = 0
            for i, image in enumerate(images.values()):
                with use_scope("image", clear=True):
                    offset = 0
                    all_matches = peekable(get_all_matches(wikitext, image["title"]))
                    if all_matches.peek("NO_ELEMENT") != "NO_ELEMENT":
                        put_markdown(f'## Please add alt text for: {image["title"].split(".")[-2].split(":")[-1]}')

                        put_image(image["imageinfo"][0]["url"], height="400px")
                    for match in all_matches:
                        images_edits += 1
                        with use_scope("alt", clear=True):
                            alt_text = get_alt_text(match)
                            if alt_text == "":
                                put_text("The image has no alt text please add it.")
                                text = input('Alt Text', rows=3, placeholder='Add the alt text here')

                                wikitext = update_wikitext_alt(wikitext, match, text, offset)
                                offset += len(text)
                            else:
                                put_text(f"Current alt text is: '{alt_text}'. Do you think that fits?")
                                answer = actions('Does the alt text fit?',
                                                 [{"label": 'Yes', "value": True, "color": "primary"},
                                                  {"label": 'No', "value": False,
                                                   "color": "warning"}])
                                if not answer:
                                    text = input('Suggest New Alt Text', rows=3, placeholder='Add the alt text here')
                                    wikitext = update_wikitext_alt(wikitext, match, text, offset)
                                    offset += len(text)
            if images_edits == 0:
                continue

            print(wikitext)
            while not send_edit_update(wikitext, meta):
                if not actions('Sending the updates to Wikipedia failed. Try Again?',
                                 [{"label": 'Yes', "value": True, "color": "primary"},
                                  {"label": 'No', "value": False,
                                   "color": "warning"}]):
                    break
            finished = actions("Current wiki page done. Do you want to fix another.",
                               [{"label": 'Yes', "value": False, "color": "primary"},
                                {"label": 'No', "value": True, "color": "warning"}])
            print("finished: ", finished)

    # Done
    with use_scope('wikipage', clear=True):
        put_markdown(f'# Thank you! See you next time')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main()
    user_updates()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
