#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


# noinspection PyBroadException
def connect(dbname='tournament'):
    """Connect to the PostgreSQL database.
    Returns database connection and cursor.
    """
    try:
        db = psycopg2.connect("dbname=%s" % dbname)
        cur = db.cursor()
        return db, cur
    except:
        print "Cannot connect to database"


def deleteMatches():
    """Remove all the match records from the database."""
    db, cur = connect()
    cur.execute("TRUNCATE Matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cur = connect()
    cur.execute("TRUNCATE players CASCADE;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cur = connect()
    cur.execute("SELECT COUNT(*) FROM players;")
    cnt = cur.fetchone()[0]
    db.close()
    return cnt


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db, cur = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    params = (name,)
    cur.execute(query, params)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cur = connect()
    cur.execute("SELECT * FROM get_standings")
    res = cur.fetchall()
    db.close()
    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cur = connect()
    query = "INSERT INTO Matches (winner,loser) VALUES (%s,%s);"
    params = (winner, loser,)
    cur.execute(query, params)
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
