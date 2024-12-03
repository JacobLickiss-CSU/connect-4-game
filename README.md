# Connect Four Game Example

This is a simple Connect Four game implemented using Python and sockets.

**Status:**
1. Gameplay is fully implemented, including accepting user actions, syncing game state, declaring a winner, and allowing a player to play another round.
2. Connected clients are asked to provide a display name for the server. This information is sent to the server to begin looking for another matched player.
3. The server will listen for client connections, and will match players together after receiving a naming message.
4. The server will maintain information about ongoing matches between players, and inform the player when their opponent has left.
5. The game state is synchronized across clients through several types of messages from the server.
6. Players can alter the game state on their turn by sending move messages. The server determines if those moves are legal before implementing them.
7. Game state information is rendered to the player when it is updated from the server.
8. If either player disconnects, the game ends.
9. If a win or draw condition is detected by the server, the clients will be informed.
10. When informed of a game over for any reason, players have the option to re-queue for another game.

**How to play:**
1. **Start the server:** Run the `server.py` script.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals.
3. **Play the game:** Players take turns entering their moves. For their move, each player selects a column to drop one of their tokens in. The token falls from the top of the column, stopping at the last available slot. The first player to line four of their tokens up wins the game.
4. **Running Tests** To run automated tests, run the `tests.py` script. If all tests pass, the message "All tests passed!" will be displayed.

**Options:**
1. **Server Options** Server options include -i to set the host address and -p to set the port. Use -h or --help for more info.
2. **Client Options** Client options include -i to set the server address, -p to set the server port, and -n to set the server DNS address. If -n is used, it will take priority over -i. Use -h or --help for more info.

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [[Link to Python documentation](https://docs.python.org/3/)]
* [[Link to sockets tutorial](https://docs.python.org/3/library/socket.html)]

**Security/Risk Evaluation**
There exists some security improvements which could be made. Currently, the client and server both assume that the official counterpart is running on the other end. Adding checks to verify that the format of the data coming in is correct, and that it is not maliciously formatted, would improve security. Some potential malicious formats would be sending an extremely long message, a message shorter than the minimum header size, or a message with an incorrect data length. The server does check for valid moves from the client, so game state security at least does not rely on the client being honest. However, very little is verified by the client of what comes in from the server, so a malicious server might be able to find a way to inject something malicious to cause the client to behave abnormally. All of these issues could be addressed by both sides of the connection not trusting the incoming data and more cautiously verifying it.

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
