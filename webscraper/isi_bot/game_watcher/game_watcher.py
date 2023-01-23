from isi_bot.game_watcher.game import Spiel, Game, SpielInfo

import requests
from bs4 import BeautifulSoup

import re
import os
from pathlib import Path
from datetime import datetime

URLS = ["https://bettv.tischtennislive.de/?L1=Ergebnisse&L2=TTStaffeln&L2P=17141&L3=Spielplan&L3P=1",
        "https://bettv.tischtennislive.de/?L1=Ergebnisse&L2=TTStaffeln&L2P=17141&L3=Spielplan&L3P=2"
        ]

CACHE_FOLDER = Path("cache")


def get_table_with_k_rows(soup, k):
    tables = soup.find_all('table')

    tables = [table for table in tables if len(
        table.find("tr").find_all(['td', 'th'])) == k]

    return tables


def get_soup(url, offline):
    # check if cahce folder exists
    if not os.path.exists(CACHE_FOLDER):
        os.makedirs(CACHE_FOLDER)

    cache_path = CACHE_FOLDER / url.replace("/", "_")
    if offline and os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
    else:
        print("Website not cached or online mode active. Querying website: " + url)
        # query website with beautiful soup
        page = requests.get(url)
        # save page.content to file
        with open(cache_path, "wb") as f:
            f.write(page.content)
        soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_all_spiel_rows(text="Olympischer SC", offline=True):
    """
    Returns a list of (url, row) tuples where row is a bs4 element. Row needs to be Spiel row contain text.
    """
    all_rows = []
    for url in URLS:
        soup = get_soup(url, offline)

        # get all table rows containing the olympischer sc
        rows = soup.find_all(lambda tag: any(td.text == text for td in tag.find_all('td')
                                             if (tag.name == 'tr' and tag.get('id') is not None and tag.get('id').startswith('Spiel'))))

        rows = [(url, row) for row in rows]
        # filter out all rows only with Vorbericht
        all_rows.extend(rows)
    return all_rows


def get_spielberichte_url(offline=True):
    def get_base_url(url):
        return url.split("/")[0] + "//" + url.split("/")[2]

    rows = get_all_spiel_rows(text="Olympischer SC", offline=offline)
    # filter out all rows only with Vorbericht
    rows = [(url, row) for url, row in rows if len(
        row.find_all(text="Vorbericht")) == 0]

    # find all links in the rows
    spielberichte = [(url, row.find_all("a", href=re.compile("Ergebnisse"))[
                      0].get('href')) for url, row in rows]
    # get base url of URL
    spielberichte_urls = [get_base_url(
        url) + spielbericht for url, spielbericht in spielberichte]
    return spielberichte_urls


def get_spielbericht_content(url, offline=True):
    spielbericht_content = {}
    soup = get_soup(url, offline=offline)
    # extract team names
    rows = soup.find_all(lambda tag: any(td.text == 'A' for td in tag.find_all('td', recursive=False)
                                         if (tag.name == 'tr')))

    if len(rows) != 1:
        print("Error: more than one team A found")
        return
    row = rows[0]
    # get all children of the row
    children = row.findChildren("td", recursive=False)
    # get the second child and fourth child
    spielbericht_content["team_a"] = children[1].text
    spielbericht_content["team_b"] = children[3].text

    # TODO extract score
    # get text of element with id "GesPunkte"
    score = soup.find(id="GesPunkte").text
    spielbericht_content["score_a"] = int(score.split(":")[0])
    spielbericht_content["score_b"] = int(score.split(":")[1])
    sets = soup.find(id="GesSatz").text
    spielbericht_content["sets_a"] = int(sets.split(":")[0])
    spielbericht_content["sets_b"] = int(sets.split(":")[1])
    balls = soup.find(id="GesBall").text
    spielbericht_content["balls_a"] = int(balls.split(":")[0])
    spielbericht_content["balls_b"] = int(balls.split(":")[1])
    # TODO extract date
    date_row = soup.find_all(lambda tag: any(td.text == 'Datum' for td in tag.find_all('td', recursive=False)
                                             if (tag.name == 'tr')))
    date_row = date_row[0].find_next_sibling()
    spielbericht_content["date"] = date_row.findChildren("td", recursive=False)[
        1].text
    # TODO extract all games Isi played in
    game_table = get_table_with_k_rows(soup, 12)[0]
    # get all rows of the table which have an input field with name Isi
    isi_games = game_table.find_all(lambda tag: any(td.find("input", {"value": "Ritz, Isabel"}) for td in tag.find_all('td', recursive=False)
                                                    if (tag.name == 'tr')))
    isi_game_content = []
    for game in isi_games:
        game_content = {}
        cols = game.find_all("td", recursive=True)
        inputs = game.find_all("input", recursive=True)
        game_content["player_a"] = inputs[0].get("value")
        game_content["player_b"] = inputs[1].get("value")

        for i in range(5):
            if cols[4 + i].text == '\xa0':
                continue
            game_content[f"set_{i+1}_score_player_a"] = int(
                cols[4 + i].text.split(":")[0])
            game_content[f"set_{i+1}_score_player_b"] = int(
                cols[4 + i].text.split(":")[1])

        game_content["sets_player_a"] = int(cols[10].text.split(":")[0])
        game_content["sets_player_b"] = int(cols[10].text.split(":")[1])
        game_content["score_player_a"] = int(cols[11].text.split(":")[0])
        game_content["score_player_b"] = int(cols[11].text.split(":")[1])
        isi_game_content.append(Game(game_content))

    spielbericht_content["isi_games"] = isi_game_content
    return Spiel(spielbericht_content)


def get_spielberichte_content(url):
    spielberichte = []
    for url in url:
        spielberichte.append(get_spielbericht_content(url))

    return spielberichte


def get_all_spiele(text="Olympischer SC", offline=True):
    spiele_rows = get_all_spiel_rows(text=text, offline=offline)
    spiele = []
    for _, row in spiele_rows:
        spiel = {}
        cols = row.find_all("td", recursive=True)
        spiel["kw"] = cols[1].text
        spiel["weekday"] = cols[3].text
        spiel["date"] = cols[4].text
        spiel["time"] = cols[6].text
        datetime_str = spiel["date"] + " " + spiel["time"]
        # convert time to datetime
        datetime_object = datetime.strptime(datetime_str, "%d.%m.%y %H:%M")
        spiel["datetime"] = datetime_object
        spiel["team_a"] = cols[7].text
        spiel["team_b"] = cols[8].text
        spiel["score"] = cols[9].find("a").text

        spiele.append(SpielInfo(spiel))

    spiele.sort()
    return spiele
