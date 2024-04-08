import os
import re

class QuakeParser:
    def __init__(self):
        self.log = self.load_log()
        self.games = self.parse_games()

    def load_log(self):
        log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "quake.txt")
        with open(log_path, "r") as file:
            return file.readlines()

    def parse_games(self):
        games = []
        game_id = -1
        for line in self.log:
            if "InitGame" in line:
                game_id += 1
                match = {
                    "id": game_id,
                    "players": [],
                    "kills": {},
                    "weapons": {},
                    "history": [],
                    "total_kills": 0,
                }
                games.append(match)
            elif "Kill" in line:
                killer, murdered, weapon = self.extract_kill_info(line)
                current_game = games[game_id]
                current_game["total_kills"] += 1
                current_game["history"].append({
                    "killer": killer,
                    "murdered": murdered,
                    "weapon": weapon
                })
                self.update_kills(killer, murdered, current_game)
                self.update_players(killer, murdered, current_game)
                self.update_weapons(weapon, current_game)
        return games

    def extract_kill_info(self, line):
        pattern = r'.*: ([^:]*?) killed (.*?) by'
        match = re.search(pattern, line)
        return match.group(1), match.group(2), line.split()[-1].strip()

    def update_kills(self, killer, murdered, current_game):
        if killer == "<world>":
            current_game["kills"][murdered] = current_game["kills"].get(murdered, 0) - 1
        elif killer == murdered:
            current_game["kills"][killer] = current_game["kills"].get(killer, 0) - 1
        else:
            current_game["kills"][killer] = current_game["kills"].get(killer, 0) + 1

    def update_players(self, killer, murdered, current_game):
        if killer != "<world>" and killer not in current_game["players"]:
            current_game["players"].append(killer)
        if murdered not in current_game["players"]:
            current_game["players"].append(murdered)

    def update_weapons(self, weapon, current_game):
        current_game["weapons"][weapon] = current_game["weapons"].get(weapon, 0) + 1
