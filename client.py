#!/usr/bin/env python3

import argparse
import sys
import socket
import selectors
import traceback
import struct

import cmanager
from message import Message

# Create the argument parser
parser = argparse.ArgumentParser(
    prog = "Connect Four Game Client",
    description= "A client for the connect four network game."
)
# Add arguments to the parser
parser.add_argument('-i', '--ip', help="The server IP address.", default="127.0.0.1") 
parser.add_argument('-p', '--port', help="The server port.", default=65432)
parser.add_argument('-n', '--DNS', help='DNS name of the server.')
# Parse arguments
args = parser.parse_args()

try:
    parsed = int(args.port)
    if(parsed < 0 or parsed > 65535):
        print("Port must be a valid integer between 1 and 65535!")
except ValueError:
    print("Port must be a valid integer between 1 and 65535!")

sel = selectors.DefaultSelector()

def run_client():
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                if(key.data is None):
                    raise Exception("No client manager found!")
                else:
                    manager = key.data
                    try:
                        manager.process(mask)
                    except Exception:
                        print("Exception in connection with ", f"{manager.address}:\n{traceback.format_exc()}")
                        manager.close()
            # Watch for closed sel
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("Closing client...")
    finally:
        sel.close()

def begin_client():
    address = (args.DNS if args.DNS else args.ip, int(args.port))
    print("Connecting to ", f"{address} ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(address)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    manager = cmanager.ClientManager(sel, sock, address)
    sel.register(sock, events, data=manager)
    name = input("Enter a display name: ")
    manager.player.name = name
    message = Message(Message.NAME, name)
    manager.schedule_message(message.pack())
    run_client()

begin_client()