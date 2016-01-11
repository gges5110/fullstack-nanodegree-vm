-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
CREATE TABLE players ( id SERIAL,
                      name TEXT DEFAULT NULL,
                      PRIMARY KEY(id));

CREATE TABLE matches ( id SERIAL,
                     winner INT,
                     loser INT,
                     PRIMARY KEY(id));
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
