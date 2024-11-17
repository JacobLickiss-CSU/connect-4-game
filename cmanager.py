import sys
import selectors
import socket
import json
import io
import struct

import connectionmanager
from gamestate import GameState
from message import Message
from playerstate import PlayerState

class ClientManager(connectionmanager.Manager):
    def __init__(self, selector, sock, address):
        super().__init__(selector, sock, address)
        self.player = PlayerState()
        self.state = GameState()

    def post_read(self):
        # Read messages from the buffer
        if(self._read_buffer):
            messages, self._read_buffer = Message.parse(self._read_buffer)
            # Handle some messages in the manager
            for message in messages:
                if(message.message_type == Message.OVER):
                    print("The game has ended! Reason: " + message.content)
                    self.request_replay()
                if(message.message_type == Message.INFO):
                    self.set_symbol(message.content)
                if(message.message_type == Message.HALT):
                    print(message.content)
                if(message.message_type == Message.PLYR):
                    self.set_opponent(message.content)
                self.state.apply_message_client(message)
                if(message.message_type == Message.TURN and message.content == self.state.symbol):
                    self.get_player_input()
                elif(message.message_type == Message.TURN):
                    print("Waiting for opponent's move...")
                if(message.message_type == Message.REDO and message.content.split(":")[0] == self.state.symbol):
                    print(message.content.split(":")[1])
                    self.get_player_input()


    def set_symbol(self, symbol):
        print("Player symbol set to " + symbol)
        self.state.symbol = symbol
        if(symbol == GameState.A):
            self.state.player_a = self.player
        else:
            self.state.player_b = self.player

    
    def set_opponent(self, packed):
        print("Player opponent data received!")
        if(self.state.symbol == GameState.A):
            self.state.player_b = PlayerState.unpack(packed)
        else:
            self.state.player_a = PlayerState.unpack(packed)
                

    def get_player_input(self):
        column = input("Enter the column to drop your token (1-7): ")
        parsed = None
        while parsed is None:
            try:
                parsed = int(column)
                if(parsed < 1 or parsed > 7):
                    parsed = None
                    column = input("Try again (1-7): ")
            except(ValueError):
                column = input("Try again (1-7): ")
        self.schedule_message(Message(Message.MOVE, column).pack())

    
    def request_replay(self):
        replay = self.get_player_replay()
        if(replay):
            self.schedule_message(Message(Message.REPL, "1").pack())
        else:
            self.close()


    def get_player_replay(self):
        response = input("Queue for another match? (y/n): ")
        parsed = None
        while parsed is None:
            if(response == "y" or response == "Y" or response == "yes"):
                parsed = True
            elif(response == "n" or response == "N" or response == "no"):
                parsed = False
            else:
                response = input("Queue for another match? (y/n): ")
        return parsed
