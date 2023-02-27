from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import numpy as np

from typing import Dict, List
from operator import itemgetter
from urllib.parse import urljoin
import os
import re

from requesting_urls import get_html

## --- Task 8, 9 and 10 --- ##


try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"



def find_best_players(url: str) -> None:
    """Finds the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    """

    teams = get_teams(url)
    all_players = {}

    for team in teams:
        name = team["name"]
        players = get_players(team["url"])
        all_players[name] = players

    player_stats = {}
    
    for team, players in all_players.items():
        player_dicts = []
        for player in players:
            stats = get_player_stats(player["url"], team)
            player_dicts.append({"name": player["name"], "url": player["url"], "points": stats["points"], "assists": stats["assists"], "rebounds": stats["rebounds"]})
        
        player_stats[team] = player_dicts

    top3_points = find_top_3("points", all_players, player_stats)
    top3_assists = find_top_3("assists", all_players, player_stats)
    top3_rebounds = find_top_3("rebounds", all_players, player_stats)

    best = [top3_points, top3_assists, top3_rebounds]
    stats_to_plot = ["points", "assists", "rebounds"]

    for b, s in zip(best, stats_to_plot):
        plot_best(b, s)


def find_top_3(stat, all_players, player_stats):
    """Finds the top 3 players from every team based on a given stat.

    arguments:
        - stat (str): which stat to use
        - all_players (dict): dictionary containing all players
        - player_stats (dicts): dictionary containing the players name, urls, and stats (points, assists, rebounds)
    returns:
        - best (dict): dictionary containing the top 3 players from each team based on given stat
    
    """

    best = {}

    for team, _ in all_players.items():
        top_3 = []

        players_with_points = []
        for player in player_stats[team]:
            if stat in player.keys():
                players_with_points.append(player)
        
        sorted_by_points = sorted(players_with_points, key=itemgetter(stat))
        
        top_3.append(sorted_by_points[-1])
        top_3.append(sorted_by_points[-2])
        top_3.append(sorted_by_points[-3])
        best[team] = top_3

    return best

def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """

    stats_dir = "NBA_player_statistics"
    teams = best

    def plot_NBA_player_statistics(teams, stat="points"):
        """Copied from example-plot.py"""

        count_so_far = 0
        all_names = []

        plt.clf()

        for team, players in teams.items():
            stats = []
            names = []

            for player in players:
                names.append(player["name"])
                stats.append(player[stat])
            all_names.extend(names)

            x = range(count_so_far, count_so_far + len(players))
            count_so_far += len(players)
            bars = plt.bar(x, stats, label=team)
            plt.bar_label(bars, label_type="edge", padding=0, fontsize=6)

        plt.xticks(range(len(all_names)), all_names, rotation=90)
        plt.legend(bbox_to_anchor=(1, 1), loc="best", borderaxespad=0, fontsize=9)
        plt.tight_layout()
        plt.grid(False)
        plt.title(stat + " per game")
        filename = stat
        print(f"Creating {filename}")

        if not os.path.isdir(stats_dir):
            os.makedirs(stats_dir)

        plt.savefig(stats_dir + "/" + filename, bbox_inches="tight")

    plot_NBA_player_statistics(teams, stat)

def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    rows = table.find_all("tr")
    rows = rows[2:]
    seed_pattern = re.compile(r"^[EW][1-8]$")

    team_links = {}  
    in_semifinal = set()  

    for row in rows:
        cols = row.find_all("td")

        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    assert len(in_semifinal) == 8

    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals
    
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """

    print(f"Finding players in {team_url}")

    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "toccolours"}).find_next("table")

    players = set()
    name_links = {}

    rows = table.find_all("tr")
    rows = rows[1:]

    for row in rows:
        cols = row.find_all("td")
        player_col = cols[2]
        a = player_col.find("a")
        name_links[player_col.get_text(strip=True)] = urljoin(base_url, a["href"])
        players.add(player_col.get_text(strip=True))

    return [
        {
            "name": player_name.rstrip("*"),
            "url": name_links[player_name],
        }
        for player_name in players
    ]


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team.
    
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
        
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """

    print(f"Fetching stats for player in {player_url}")

    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="NBA")

    if not table:
        table = soup.find(id="Regular_season")

    table_NBA = table.find_next("table", {"class": "wikitable"})
    
    RPG_col = ''
    APG_col = ''
    PPG_col = ''

    rows = table_NBA.find_all("tr")
    rows = rows[1:]
    headings = table_NBA.find_all("th")
    head_title = [th.text.strip() for th in headings]

    RPG_index = head_title.index("RPG") 
    APG_index = head_title.index("APG")
    PPG_index = head_title.index("PPG")

    for row in rows:
        cols = row.find_all("td")

        seasons = cols[0].find("a")
        if seasons is not None:
            season = seasons.get("title")
            if season == '2021–22 NBA season':
                team_name = cols[1].get_text(strip=True)
                if team_name != team:
                    continue
                else:
                    RPG_col = cols[RPG_index].get_text().rstrip('*')
                    APG_col = cols[APG_index].get_text().rstrip('*')
                    PPG_col = cols[PPG_index].get_text().rstrip('*').rstrip("\n")

    if RPG_col == '' or APG_col == '' or 'PPG_col' == '':
        stats = {"rebounds": 0, "assists": 0, "points": 0}
    else:
        stats = {"rebounds": float(RPG_col.rstrip('*')), "assists": float(APG_col.rstrip('*')), "points": float(PPG_col.rstrip('*'))}
    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
