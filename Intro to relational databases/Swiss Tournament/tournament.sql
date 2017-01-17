-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- TABLES CREATION
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

CREATE TABLE Players (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(100)
);

CREATE TABLE Matches (
  id     SERIAL PRIMARY KEY,
  winner INT,
  loser  INT,
  FOREIGN KEY (winner) REFERENCES Players (id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (loser) REFERENCES Players (id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- VIEW TO GET THE STANDINGS
DROP VIEW IF EXISTS get_standings;
CREATE VIEW get_standings
AS
  SELECT
    player_total.sid    AS id,
    player_total.name   AS name,
    coalesce(wins, 0)  AS wins,
    coalesce(loses, 0) AS matches
  FROM
    (SELECT
       p.id         AS sid,
       p.name       AS name,
       count(loser) AS loses
     FROM Players p LEFT JOIN matches m ON p.id = m.loser or p.id = m.winner
     GROUP BY p.id, name
     ORDER BY p.id) AS player_total
    JOIN
    (SELECT
       p.id          AS sid,
       count(winner) AS wins
     FROM Players p LEFT JOIN matches m ON p.id = m.winner
     GROUP BY p.id
     ORDER BY p.id) AS player_wins ON player_total.sid = player_wins.sid
  ORDER BY wins;

SELECT * FROM get_standings;
