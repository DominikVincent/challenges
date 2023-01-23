class Spiel():
    """
    A wrapper around a dict to implement a more convenient interface to the data.
    A Spiel consists of several games. Each game consists of several sets. Each set consists of several balls.
    """

    def __init__(self, spiel_dict):
        self.spiel_dict = spiel_dict

    def get_date(self):
        return self.spiel_dict["date"]

    def get_winning_team(self):
        if self.spiel_dict["score_a"] == self.spiel_dict["score_b"]:
            return "draw"
        return self.spiel_dict["team_a"] if self.spiel_dict["score_a"] > self.spiel_dict["score_b"] else self.spiel_dict["team_b"]

    def get_loosing_team(self):
        if self.spiel_dict["score_a"] == self.spiel_dict["score_b"]:
            return "draw"
        return self.spiel_dict["team_a"] if self.spiel_dict["score_a"] < self.spiel_dict["score_b"] else self.spiel_dict["team_b"]

    def get_winning_team_score(self):
        return self.spiel_dict["score_a"] if self.spiel_dict["score_a"] > self.spiel_dict["score_b"] else self.spiel_dict["score_b"]

    def get_loosing_team_score(self):
        return self.spiel_dict["score_a"] if self.spiel_dict["score_a"] < self.spiel_dict["score_b"] else self.spiel_dict["score_b"]

    def get_games(self):
        return self.spiel_dict["isi_games"]

    def isi_wins(self):
        count = 0
        total = 0
        for game in self.get_games():
            total += 1
            if game.did_isi_win():
                count += 1
        return count, total

    def __repr__(self):
        return self.spiel_dict.__repr__()

    def __str__(self):
        if self.get_winning_team() == "draw":
            team_a = self.spiel_dict["team_a"]
            team_b = self.spiel_dict["team_b"]
            opening_line = f"Am {self.get_date()} gab es ein Unentschieden zwischen {team_a} and {team_b}.\n"
        else:
            opening_line = f"Am {self.get_date()} hat {self.get_winning_team()} {self.get_winning_team_score()}:{self.get_loosing_team_score()} gegen {self.get_loosing_team()} gewonnen.\n"
        isi_wins, isi_plays = self.isi_wins()
        isi_line = f"Isi hat auch mit gespielt und {isi_wins}/{isi_plays} Spiele gewonnen.\n" if isi_plays > 0 else "Isi hat nicht mitgespielt. Tststs. \n"
        congrats_line = f"Guter Beitrag für das Team, Isi!\n" if isi_wins > isi_plays / \
            2 else f"Schade, Isi. Nächstes Mal besser!\n"

        #games = "\n".join([game.__str__() for game in self.get_matches()])

        return opening_line + isi_line + congrats_line


class Game():
    """
    A wrapper around a dict to implement a more convenient interface to the data. This is a part of a Spiel.
    """

    def __init__(self, game_dict):
        self.game_dict = game_dict

    def get_winning_player(self):
        if self.game_dict["score_player_a"] == self.game_dict["score_player_b"]:
            return "draw"
        return self.game_dict["player_a"] if self.game_dict["score_player_a"] > self.game_dict["score_player_b"] else self.game_dict["player_b"]

    def get_loosing_player(self):
        if self.game_dict["score_player_a"] == self.game_dict["score_player_b"]:
            return "draw"
        return self.game_dict["player_a"] if self.game_dict["score_player_a"] < self.game_dict["score_player_b"] else self.game_dict["player_b"]

    def get_winning_player_score(self):
        return self.game_dict["score_player_a"] if self.game_dict["score_player_a"] > self.game_dict["score_player_b"] else self.game_dict["score_player_b"]

    def get_loosing_player_score(self):
        return self.game_dict["score_player_a"] if self.game_dict["score_player_a"] < self.game_dict["score_player_b"] else self.game_dict["score_player_b"]

    def get_winning_player_sets(self):
        return self.game_dict["sets_player_a"] if self.game_dict["sets_player_a"] > self.game_dict["sets_player_b"] else self.game_dict["sets_player_b"]

    def get_loosing_player_sets(self):
        return self.game_dict["sets_player_a"] if self.game_dict["sets_player_a"] < self.game_dict["sets_player_b"] else self.game_dict["sets_player_b"]

    def get_winning_player_set_score(self, set_number):
        return self.game_dict[f"set_{set_number}_score_{self.winning_player_is_player()}"]

    def get_loosing_player_set_score(self, set_number):
        return self.game_dict[f"set_{set_number}_score_{self.loosing_player_is_player()}"]

    def winning_player_is_player(self):
        if self.get_winning_player() == self.game_dict["player_a"]:
            return "player_a"
        elif self.get_winning_player() == self.game_dict["player_b"]:
            return "player_b"
        else:
            return "player_unknown"

    def loosing_player_is_player(self):
        if self.get_loosing_player() == self.game_dict["player_a"]:
            return "player_a"
        elif self.get_loosing_player() == self.game_dict["player_b"]:
            return "player_b"
        else:
            return "player_unknown"

    def get_set_winner(self, set_number):
        return self.game_dict["player_a"] if self.game_dict[f"set_{set_number}_score_player_a"] > self.game_dict[f"set_{set_number}_score_player_b"] else self.game_dict["player_b"]

    def did_isi_win(self):
        return self.get_winning_player() == "Ritz, Isabel"

    def __repr__(self):
        return self.game_dict.__repr__()

    def __str__(self):
        opening_line = "Wuhu Isi hat dieses Spiel gewonnen\n" if self.did_isi_win(
        ) else "Schade, Isi hat dieses Spiel verloren. Da muss sie wohl noch gegen Philipp üben.\n"
        match_description = f"{self.get_winning_player()} hat gegen {self.get_loosing_player()} mit *{self.get_winning_player_sets()}*:{self.get_loosing_player_sets()} gewonnen.\n"
        set_description = "\n".join([f"Im {i+1}. Satz hat {self.get_set_winner(i+1)} {self.get_winning_player_set_score(i+1)}:{self.get_loosing_player_set_score(i+1)} gewonnen. " for i in range(
            self.get_loosing_player_sets() + self.get_winning_player_sets())])

        return opening_line + match_description + set_description


class SpielInfo():
    def __init__(self, spiel_info_dict):
        self.spiel_info_dict = spiel_info_dict

    def __getitem__(self, item):
        return self.spiel_info_dict[item]

    def __lt__(self, other):
        return self.spiel_info_dict["datetime"] < other.spiel_info_dict["datetime"]

    def __gt__(self, other):
        return self.spiel_info_dict["datetime"] > other.spiel_info_dict["datetime"]

    def __repr__(self) -> str:
        return self.spiel_info_dict.__repr__()

    def __str__(self) -> str:
        spiel_info_str = f"Am {self.spiel_info_dict['weekday']} den {self.spiel_info_dict['date']} um {self.spiel_info_dict['time']} Uhr \
spielt {self.spiel_info_dict['team_a']} gegen {self.spiel_info_dict['team_b']}."
        return spiel_info_str
