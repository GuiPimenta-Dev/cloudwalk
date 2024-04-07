import json
from dataclasses import dataclass
import quake_parser

@dataclass
class Input:
    pass

@dataclass
class Output:
    message: str


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