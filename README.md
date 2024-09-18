# Connect Four Game Example

This is a simple Connect Four game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals.
3. **Play the game:** Players take turns entering their moves. For their move, each player selects a column to drop one of their tokens in. The token falls from the top of the column, stopping at the last available slot. The first player to line four of their tokens up wins the game.

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [[Link to Python documentation](https://docs.python.org/3/)]
* [[Link to sockets tutorial](https://docs.python.org/3/library/socket.html)]

# SOW (Statement Of Work)

**Project Title:**

Connect Four Game

**Team:**

Jacob Lickiss

**Project Objective:**

The goal of this project is to produce a proof-of-concept multiplayer video game which uses low-level networking sockets in python. The game itself will be a simple connect four game, with a server and two clients.

**Scope:**

*Inclusions:*
1. A server which will fascilitate the game between two players.
2. A client which can connect to the server and play with another client.
3. A simple terminal interface to interact with the game.
4. Command line options which provide documentation on the game and utilities for the connection.

*Exclusions*
1. A GUI for the server, client, or game.
2. Support for less or more than two client players.
3. An AI to play the game against, if another player is not available.
4. Matchmaking between N clients.
5. A magic machine that solves all your problems.

**Deliverables**
1. A server.py script to start the server.
2. A client.py script to start the client.
3. A README with detailed play instructions.
4. A small automated testing suite.
5. Possibly a presentation of some form, requirements unclear.

**Timeline**

*Key Milestones*
+ Sprint 0 (Sep 22) - Basic setup, teams, Github, VSCode, SOW.
+ Sprint 1 (Oct 06) - Client/server, sockets
+ Sprint 2 (Oct 20) - Application layer development, connection management
+ Sprint 3 (Nov 03) - Synchronized state, multi-client features
+ Sprint 4 (Nov 17) - Gameplay, game interface
+ Sprint 5 (Dec 06) - Error handling and automated tests

*Tasks*
1. Create repository and basic script files: 1.5 hours
2. Implement basic client/server connection using TCP: 2 hours
3. Implement multiple client/server connections: 3 hours
4. Create client/server application layer protocol: 2 hours
5. Generic state synchronization: 2 hours
6. Gameplay state implementation: 1.5 hours
7. Build game terminal interface: 2 hours
8. Win/lose state handling: 1 hour
9. Error detection and handling: 2.5 hours
10. Build automated connection tests: 1.5 hours
11. Build automated gameplay tests: 2 hours

**Technical Requirements**

*Hardware*
+ One or more python capable computers.
+ Monitor and keyboard for each machine.
+ A network connection between all client/server machines.

*Software*
+ Python stack.
+ Terminal access.
+ The server machine must have an accessible IP address and port.

**Assumptions**

1. The clients and server can be run on one machine or spread over multiple.
2. Since the client and server are written in python, the software should be compatible with a wide range of machines.
3. A stable network connection will be available between all machines.
4. The officially developed client will be used by all players.
5. The officially developed server will be used by the host.

**Roles and Responsibilities**

Jacob Lickiss - Responsible for everything. Project manager, software developer, QA, etc.

**Communication Plan**

I will check in with myself each sprint to verify that expected milestones have been hit, and adjust if they have not.

**Additional Notes**

This is developed as a class project and is not intended for use in production.
