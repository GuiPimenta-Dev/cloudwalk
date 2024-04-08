import json
import os
import pytest
from .quake_parser import QuakeParser

@pytest.fixture(scope="module")
def parser():
    return QuakeParser()

def test_load_log(parser):
    assert parser.log

def test_parse_games(parser):
    assert parser.games

def test_extract_kill_info(parser):
    line = "12:34 Kill: Player1 killed Player2 by MOD_RAILGUN"
    killer, murdered, weapon = parser.extract_kill_info(line)
    assert killer == "Player1"
    assert murdered == "Player2"
    assert weapon == "MOD_RAILGUN"

def test_update_kills(parser):
    game = {"kills": {}}
    parser.update_kills("Player1", "Player2", game)
    assert game["kills"] == {"Player1": 1}
    parser.update_kills("Player2", "Player1", game)
    assert game["kills"] == {"Player1": 1, "Player2": 1}
    parser.update_kills("<world>", "Player1", game)
    assert game["kills"] == {"Player1": 0, "Player2": 1}

def test_update_players(parser):
    game = {"players": []}
    parser.update_players("Player1", "Player2", game)
    assert game["players"] == ["Player1", "Player2"]
    parser.update_players("Player1", "Player2", game)
    assert game["players"] == ["Player1", "Player2"]

def test_update_weapons(parser):
    game = {"weapons": {}}
    parser.update_weapons("MOD_RAILGUN", game)
    assert game["weapons"] == {"MOD_RAILGUN": 1}
    parser.update_weapons("MOD_RAILGUN", game)
    assert game["weapons"] == {"MOD_RAILGUN": 2}
    parser.update_weapons("MOD_ROCKET", game)
    assert game["weapons"] == {"MOD_RAILGUN": 2, "MOD_ROCKET": 1}

def test_final_output(parser):
    current_path = os.path.dirname(os.path.realpath(__file__))
    expected_result = json.load(open(f"{current_path}/expected_result.json"))
    assert expected_result == parser.games