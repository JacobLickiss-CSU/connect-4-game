#!/usr/bin/env python3

import argparse
import sys
import socket
import selectors
import traceback

import servermatch
from smanager import ServerManager
from gamestate import GameState

# Create the argument parser
parser = argparse.ArgumentParser(
    prog = "Connect Four Game Server",
    description= "A server for the connect four network game. While running, clients can connect and play a game of connect four."
)
# Add arguments to the parser
parser.add_argument('-i', '--ip', help="The host IP address.", default="0.0.0.0") 
parser.add_argument('-p', '--port', help="The host port.", default=65432) 
# Parse arguments
args = parser.parse_args()

# Get the default selector
sel = selectors.DefaultSelector()

def accept_connection(socket):
    connection, address = socket.accept()
    connection.setblocking(False)
    manager = ServerManager(sel, connection, address)
    sel.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE, manager)
    print("Connection established with ", address)


def run_server():
    try:
        while True:
            events = sel.select(timeout=3)
            for key, mask in events:
                if(key.data is None):
                    accept_connection(key.fileobj)
                else:
                    manager = key.data
                    try:
                        manager.process(mask)
                    except Exception:
                        print("Exception in connection with ", f"{manager.address}:\n{traceback.format_exc()}")
                        servermatch.game_disconnect(manager, "Opponent disconnected.")
                        manager.close()
    except KeyboardInterrupt:
        print("Closing server...")
    finally:
        sel.close()


def begin_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.ip, int(args.port)))
    sock.listen()
    print("Server started on", (args.ip, int(args.port)))
    print("Ctrl+C to close the server.")
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)
    run_server()

begin_server()