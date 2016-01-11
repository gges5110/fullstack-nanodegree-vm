-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players ( id SERIAL,
                      name TEXT NOT NULL,
                      PRIMARY KEY(id));

CREATE TABLE matches ( id SERIAL,
                     winner INT REFERENCES players(id) ON DELETE CASCADE,
                     loser INT REFERENCES players(id) ON DELETE CASCADE CHECK (winner <> loser),
                     PRIMARY KEY(id));

 CREATE VIEW standings AS
 SELECT players.id as id, players.name,
 (SELECT count(*) FROM matches WHERE matches.winner = players.id) as won,
 (SELECT count(*) FROM matches WHERE players.id in (winner, loser)) as played
 FROM players GROUP BY players.id ORDER BY won DESC;
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
