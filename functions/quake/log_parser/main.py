import json
from dataclasses import dataclass
import quake_parser
from typing import List, Dict

@dataclass
class Input:
    pass

@dataclass
class History:
    killer: str
    murdered: str
    weapon: str

@dataclass
class Game:
    total_kills: int
    players: List[str]
    kills: Dict[str, int]
    ranking: List[str]
    history: List[History]
    kills_by_means: Dict[str, int]  

@dataclass
class Output:
    data: Dict[str, Game]


def lambda_handler(event, context):
    matches = quake_parser.QuakeParser().games
    games = {}
    for match in matches:
        ranking = sorted(match["players"], key=lambda player: match["kills"].get(player, 0), reverse=True)
        games[f"game_{match['id']}"] = {
            "total_kills": match["total_kills"],
            "players": match["players"],
            "kills": match["kills"],
            "ranking": ranking,
            "history": match["history"],
            "kills_by_means": match["weapons"]
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"data": games})
    }
