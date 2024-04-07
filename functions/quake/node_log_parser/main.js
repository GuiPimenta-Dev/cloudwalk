const QuakeParser = require("./parser");

exports.handler = async (event, context) => {
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

    return {
      statusCode: 200,
      body: JSON.stringify({ data: games }),
      headers: {
        "Content-Type": "application/json",
      },
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal Server Error" }),
      headers: {
        "Content-Type": "application/json",
      },
    };
  }
};
