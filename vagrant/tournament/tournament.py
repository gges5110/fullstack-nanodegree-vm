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
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("delete from matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("delete from players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("select count(*) from players")
    num = cur.fetchall()[0][0]
    conn.close()
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s)", (name, ))
    conn.commit()
    conn.close()


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
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("select * from players")
    players = ({
            'id': str(row[0]),
            'name': str(row[1])}
            for row in cur.fetchall())
    player_list = []
    for player in players:
        id = int(player['id'])
        # print 'player id = ' + str(id)
        cur.execute("select count(*) from matches where winner = %d" % id)
        wins = cur.fetchall()[0][0]
        cur.execute("select count(*) from matches where winner = %d or loser = %d" % (id, id))
        matches = cur.fetchall()[0][0]
        player_tuple = (player['id'], player['name'], int(wins), int(matches))
        player_list.append(player_tuple)
    player_list = sorted(player_list, key=lambda player: player[2])
    # print player_list
    conn.close()
    return player_list

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("INSERT INTO matches (winner, loser) VALUES (%d, %d)" % (int(winner), int(loser)))
    conn.commit()
    conn.close()


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
    match_list = []
    for i in range(0, len(standings), 2):
        tup = (standings[i][0], standings[i][1], standings[i + 1][0], standings[i + 1][1])
        match_list.append(tup)
        # print tup
    return match_list
