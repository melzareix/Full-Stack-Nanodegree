-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- TABLES CREATION
DROP TABLE IF EXISTS Players CASCADE;
CREATE TABLE Players (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(100)
);

DROP TABLE IF EXISTS Standings;
CREATE TABLE Standings (
  id      INT,
  wins    INT DEFAULT 0,
  loses   INT DEFAULT 0,
  matches INT DEFAULT 0,
  FOREIGN KEY (id) REFERENCES Players (id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Matches;
CREATE TABLE Matches (
  id     SERIAL PRIMARY KEY,
  winner INT,
  loser  INT,
  FOREIGN KEY (winner) REFERENCES Players (id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (loser) REFERENCES Players (id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- CREATING TRIGGERS

-- TRIGGER TO INSERT THE NEWLY CREATED PLAYER TO
-- THE STANDINGS TABLE.

DROP FUNCTION IF EXISTS insert_player_to_standings();
CREATE OR REPLACE FUNCTION insert_player_to_standings()
  RETURNS TRIGGER AS
$$
BEGIN
  INSERT INTO Standings (id) VALUES (NEW.id);
  RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER player_inserted AFTER INSERT
  ON Players
FOR EACH ROW
EXECUTE PROCEDURE insert_player_to_standings();

INSERT INTO Players (name) VALUES ('ali');
INSERT INTO Players (name) VALUES ('mohamed');

TRUNCATE Matches;