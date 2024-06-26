const express = require("express");
const bodyParser = require("body-parser");
const QuakeParser = require("./quake");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

app.get("/games", (req, res) => {
  try {
    const matches = new QuakeParser().games;
    const games = {};

    for (const match of matches) {
      const ranking = match.players.sort(
        (a, b) => (match.kills[b] || 0) - (match.kills[a] || 0)
      );
      games[`game_${match.id}`] = {
        total_kills: match.total_kills,
        players: match.players,
        kills: match.kills,
        ranking: ranking,
        history: match.history,
        kills_by_means: match.weapons,
      };
    }

    res.status(200).json({ data: games });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
