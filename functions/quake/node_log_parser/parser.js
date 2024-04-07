const fs = require("fs");
const path = require("path");

class QuakeParser {
  constructor() {
    this.log = this.loadLog();
    this.games = this.parseGames();
  }

  loadLog() {
    const logPath = path.join(__dirname, "quake.log");
    return fs.readFileSync(logPath, "utf-8").split("\n");
  }

  parseGames() {
    const games = [];
    let gameId = -1;

    for (let line of this.log) {
      if (line.includes("InitGame")) {
        gameId++;
        const match = {
          id: gameId,
          players: [],
          kills: {},
          weapons: {},
          history: [],
          total_kills: 0,
        };
        games.push(match);
      } else if (line.includes("Kill")) {
        const [killer, murdered, weapon] = this.extractKillInfo(line);
        const currentGame = games[gameId];
        currentGame.total_kills++;
        currentGame.history.push({ killer, murdered, weapon });
        this.updateKills(killer, murdered, currentGame);
        this.updatePlayers(killer, murdered, currentGame);
        this.updateWeapons(weapon, currentGame);
      }
    }

    return games;
  }

  extractKillInfo(line) {
    const pattern = /.*: ([^:]*?) killed (.*?) by/;
    const match = line.match(pattern);
    return [match[1], match[2], line.split(" ").slice(-1)[0].trim()];
  }

  updateKills(killer, murdered, currentGame) {
    if (killer === "<world>") {
      currentGame.kills[murdered] = (currentGame.kills[murdered] || 0) - 1;
    } else if (killer === murdered) {
      currentGame.kills[killer] = (currentGame.kills[killer] || 0) - 1;
    } else {
      currentGame.kills[killer] = (currentGame.kills[killer] || 0) + 1;
    }
  }

  updatePlayers(killer, murdered, currentGame) {
    if (killer !== "<world>" && !currentGame.players.includes(killer)) {
      currentGame.players.push(killer);
    }
    if (!currentGame.players.includes(murdered)) {
      currentGame.players.push(murdered);
    }
  }

  updateWeapons(weapon, currentGame) {
    currentGame.weapons[weapon] = (currentGame.weapons[weapon] || 0) + 1;
  }
}

module.exports = QuakeParser;
