Intro to Relational Databases
=============

<h2>Setup Environment</h2>
First we need to provide an environment for the database to run on. The cloned repo is already a Vagrant environment. For convinience, install Vagrant along with Virtualbox to save your time configuring operating system and libraries. Then clone this repo and use Git bash to start Vagrant at the cloned repo directory. For example,
```
cd path/to/your/repo
vagrant up
```
This will start up a Ubuntu machine in virtual box, you can check if it is running by using the command
```
vagrant status
```
This will show you the status of the machines that are currently running. To ssh into the virtual machine, use
```
vagrant ssh
```
Learn more commands at the Vagrant's documentation (https://docs.vagrantup.com/v2/cli/index.html). The following will explain how the tournament database works.

<h2>How to build up the database </h2>
Once connected to Ubuntu, cd to the tournament folder. Use the following command to build the database. It will drop existing tournament database and create a new one.
```
cd /vagrant/tournament
psql -f tournament.sql
```

<h2>How to import the database schema</h2>
To import the database shcema, simply go into the psql command line and use the \i command:
```
psql
\i tournament.sql
```

<h2>What are the required setup in order to run the application successfully</h2>
Write a client application for using the tournament library we provided. Here are the methods included:

| function name   | Description |
| :-------------- |:---------------|
| connect         | Connects to the database. |
| deleteMatches   | Remove all the matches records from the database.  |
| deletePlayers   | Remove all the player records from the database. | 
| countPlayers    | Returns the number of players currently registered.  |
| registerPlayer  | Adds a player to the tournament database.|
| playerStandings | Returns a list of the players and their win records, sorted by wins. |
| reportMatch     | Record the winner and loser of a match.
| swissPairings   | Returns a list of pairs of players for the next round of a match. The return value will a list with values: (id1, name1, id2, name2) |


<h2>How to run the test cases</h2>
Under the tournament folder there is a test file named tournament_test.py. Simply run the test by
```
python tournament_test.py
```
It should contain 8 tests for the tournament.py file.
