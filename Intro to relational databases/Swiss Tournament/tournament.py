#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("TRUNCATE Matches;")
    cur.execute("UPDATE Standings SET matches = 0, wins = 0, loses = 0")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("TRUNCATE players CASCADE;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM players;")
    cnt = cur.fetchall()[0][0]
    db.close()
    return cnt


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    cur.execute(
        "SELECT Players.id,name,wins,matches "
        "FROM Players JOIN Standings ON Players.id = Standings.id "
        "ORDER BY wins DESC;")
    res = cur.fetchall()
    db.close()
    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO Matches (winner,loser) VALUES (%s,%s);",
                (winner, loser,))
    cur.execute(
        "UPDATE Standings  SET wins = wins + 1, "
        "matches = matches + 1  WHERE id = %s",
        (winner,))
    cur.execute("UPDATE Standings  SET loses = loses + 1, "
                "matches = matches + 1  WHERE id = %s",
                (loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairing = []
    for x in xrange(0, len(standings), 2):
        player1 = standings[x]
        player2 = standings[x + 1]
        pairing.append((player1[0], player1[1], player2[0], player2[1]))
    return pairing


